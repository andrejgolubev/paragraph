// В начале loadSchedule.js
import { openHomeworkModal, initHomeworkModal } from "./dialog.js";

// ✅ Убедись что модальное окно инициализировано
document.addEventListener("DOMContentLoaded", () => {
  initHomeworkModal();
});

function getDateValueFromDisplay(dateDisplay) {
  // Пример: "17 ноября" -> "2025-11-17"
  const months = {
    января: "01",
    февраля: "02",
    марта: "03",
    апреля: "04",
    мая: "05",
    июня: "06",
    июля: "07",
    августа: "08",
    сентября: "09",
    октября: "10",
    ноября: "11",
    декабря: "12",
  };

  console.log(dateDisplay);
  const [day, month] = dateDisplay.split(" ");
  const year = new Date().getFullYear(); // или из scheduleData если есть
  const monthNumber = months[month];

  return `${year}-${monthNumber}-${day.padStart(2, "0")}`;
}

const convertDate = (date) => {
  return date.split("-").reverse().join(".");
};

function addHomeworkHandlers(groupDataValue, dateDataValue) {
  const homeworkButtons = document.querySelectorAll(".homework");

  console.log(`Found ${homeworkButtons.length} homework buttons`);

  homeworkButtons.forEach((hmwButton) => {
    hmwButton.addEventListener("click", function () {
      const lessonElement = hmwButton.parentElement
      const lessonName = lessonElement
        .querySelector(".lesson-text strong").textContent
        ;
      
      const lessonText = lessonElement.querySelector('.lesson-text').textContent.replace(lessonName, '').split(',').join(', ')
      const lessonIndex = lessonElement.parentElement.getAttribute("data-index");
      const lessonDay = lessonElement.parentElement.getAttribute("data-date"); //x ноября , достается из колонки

      let formHeader = document.querySelector("#homework-form h3");
      formHeader.innerHTML = `<p><strong>${lessonName}</strong>, ${lessonDay}</p> 
      
      <p>${lessonText}</p>`
      

      console.log("Homework button clicked:", { lessonIndex });
      console.log(formHeader.innerHTML);

      const lessonInfo = {
        groupDataValue: groupDataValue,
        dateDataValue: dateDataValue, // ✅ КОНКРЕТНАЯ ДАТА КОЛОНКИ
        lessonIndex: parseInt(lessonIndex),
      };

      console.log("Homework for:", {
        date: dateDataValue,
        group: groupDataValue,
        lesson: lessonText,
      });

      openHomeworkModal(lessonInfo);
    });
  });
}

function escapeHtml(unsafe) {
  // для XSS protection
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

export async function loadSchedule(groupDataValue, dateDataValue = null) {
  try {
    let url = `http://127.0.0.1:8000/schedule/get-schedule?group_data_value=${groupDataValue}`;

    if (dateDataValue) {
      url += `&date_data_value=${dateDataValue}`;
    }

    const response = await fetch(url);
    const scheduleData = await response.json();

    displaySchedule(scheduleData);
  } catch (error) {
    console.error("Error loading schedule:", error);
  }
}

function displaySchedule(scheduleData) {
  const tipElem = document.querySelector(".tip");
  const scheduleContainer = document.getElementById("schedule-container");
  scheduleContainer.className = "schedule-container loading";

  let html = `
    <table class="table">
      <thead>
        <tr class="table_row_high">
          <th>время</th>
  `;

  const datesArr = [];

  // Заголовки дней
  scheduleData.days.forEach((day) => {
    html += `
      <th>
        <p>${day.date}</p>
        <p id="week-day">${day.day}</p>
      </th>
    `;
    datesArr.push(day.date);
  });

  console.log(datesArr);
  html += `
        </tr>
      </thead>
      <tbody>
  `;
  let lessonIndex = 1;
  // Строки с расписанием
  scheduleData.schedule.forEach((timeSlot) => {
    html += `
      <tr>
        <td>
          <p>${timeSlot.time_start}</p>
          <p>${timeSlot.time_end}</p>
        </td>
    `;

    // Занятия для каждого дня (пн-сб)

    timeSlot.lessons.forEach((dayLessons) => {
      html += `<td data-date="${
        datesArr[(lessonIndex - 1) % 6]
      }" data-index="${lessonIndex}">`;
      lessonIndex++;
      if (dayLessons.length > 0) {
        dayLessons.forEach((lesson) => {
          let lessonId = "default";
          if (lesson.type === "Лек.") {
            lessonId = "lec";
          } else if (lesson.type === "Упр.") {
            lessonId = "upr";
          } else if (lesson.type === "Лаб.") {
            lessonId = "lab";
          }
          let lessonName = escapeHtml(lesson.text.split(", ")[0]);
          let lessonText = escapeHtml(lesson.text).replace(
             lesson.text.includes(", ") ? lessonName + ", " : lessonName,
            ""
          );
          

          html += `
            <div class="lesson-item" id="${lessonId}">
              ${
                lesson.type
                  ? `<span class="lesson-type ${getLessonTypeClass(
                      lesson.type
                    )}">${lesson.type}</span>`
                  : ""
              }
              <div class="homework">
                <img src="./static/static/paperclip.svg"> 
                
              </div>

              <div class="lesson-text"> <strong>${lessonName}</strong> 
              
          `;
          let toAdd = ''
          const parts = lessonText.split(',').filter(part => part.trim() !== '');

          parts.forEach((part, index) => {
            const trimmed = part.trim();
            if (index === parts.length - 1) {
              toAdd += `<p>${trimmed}</p>`;
            } else {
              toAdd += `<p>${trimmed},</p>`;
            }
          });
          
          
          html += ` 
              ${toAdd}
            </div>
          </div>
          `
        });
      } else {
        html += `<div class="lesson-empty"> </div>`;
      }

      html += `</td>`;
    });

    html += `</tr>`;
  });

  html += `
      </tbody>
    </table>
  `;

  scheduleContainer.innerHTML = html;
  tipElem.classList.remove("tip-active");

  addHomeworkHandlers(
    scheduleData.group_data_value,
    scheduleData.date_data_value
  );

  // определяем какая дата текущая
  const weekDaysMap = {
    Понедельник: 1,
    Вторник: 2,
    Среда: 3,
    Четверг: 4,
    Пятница: 5,
    Суббота: 6,
  };

  const dateObj = new Date();
  const currentWeekDay = dateObj.getDay();

  const weekDays = document.querySelectorAll("#week-day"); //nodelist

  weekDays.forEach((day) => {
    if (weekDaysMap[day.textContent] === currentWeekDay) {
      day.parentElement.classList.add("active-day");
    }
  });

  setTimeout(() => {
    scheduleContainer.className = "schedule-container loaded";
  }, 100);
}

// Вспомогательные функции для стилизации
function getLessonTypeClass(type) {
  const typeMap = {
    "Лек.": "lecture",
    "Лаб.": "lab",
    "Упр.": "practice",
  };
  return typeMap[type] || "default";
}

function getCurrentWeekDate(dayIndex) {
  const today = new Date();
  const currentDay = today.getDay();
  const diff = dayIndex - (currentDay === 0 ? 6 : currentDay - 1); // Приводим к 0-5 (пн-сб)

  const targetDate = new Date(today);
  targetDate.setDate(today.getDate() + diff);

  return targetDate.toISOString().split("T")[0]; // Формат YYYY-MM-DD
}




// let lessonName = escapeHtml(lesson.text.split(", ")[0]);
// let lessonText = escapeHtml(lesson.text).replace(
//   lessonName + ", " ? lessonName.includes(", ") : lessonName,
//   ""
// );
// console.log("lessonName:", lessonName);
// console.log("lessonText:", lessonText);
