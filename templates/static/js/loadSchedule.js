// В начале loadSchedule.js
import { openHomeworkModal, initHomeworkModal } from './dialog.js';

// ✅ Убедись что модальное окно инициализировано
document.addEventListener('DOMContentLoaded', () => {
  initHomeworkModal();
});


function addHomeworkHandlers(groupDataValue, dateDataValue) {
  const homeworkButtons = document.querySelectorAll('.homework'); 
  
  console.log(`Found ${homeworkButtons.length} homework buttons`);
  
  homeworkButtons.forEach(button => {
    button.addEventListener('click', function() {
      const dayIndex = this.getAttribute('data-day');
      const timeSlotIndex = this.getAttribute('data-time');
      const lessonIndex = this.getAttribute('data-lesson');

      const lessonText = button.parentElement.querySelector('.lesson-text').textContent.split(', ')[0]
      let formHeader = document.querySelector('#homework-form h3')
      formHeader.innerHTML = `<strong>${lessonText}</strong> <p>(${getCurrentWeekDate(dayIndex)})</p>`

      console.log('Homework button clicked:', { dayIndex, timeSlotIndex, lessonIndex });
      
      const lessonInfo = {
        groupDataValue: groupDataValue,
        dateDataValue: dateDataValue || getCurrentWeekDate(dayIndex),
        dayIndex: parseInt(dayIndex),
        timeSlotIndex: parseInt(timeSlotIndex),
        lessonIndex: parseInt(lessonIndex)
      };
      
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

  // Заголовки дней
  scheduleData.days.forEach((day) => {
    html += `
      <th>
        <p>${day.date}</p>
        <p id="week-day">${day.day}</p>
      </th>
    `;
  });

  html += `
        </tr>
      </thead>
      <tbody>
  `;

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
      html += `<td>`;

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
          let lessonName = lesson.text.split(', ')[0]
          // console.log('lessonName:', lessonName)
          html += `
            <div class="lesson-item" id="${lessonId}">
              ${
                lesson.type
                  ? `<span class="lesson-type ${getLessonTypeClass(
                      lesson.type
                    )}">${lesson.type}</span>`
                  : ""
              }
              <div class="homework"> <img src="./static/static/paperclip.svg"> </div>
              <div class="lesson-text"> <strong>${lessonName}</strong> ${escapeHtml(lesson.text).replace(lessonName, '')}</div>
            </div>
          `;
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

  addHomeworkHandlers(scheduleData.group_data_value, scheduleData.date_data_value);

  // определяем какая дата текущая
  const weekDaysMap = {
    'Понедельник': 1,
    'Вторник': 2,
    'Среда': 3,
    'Четверг': 4,
    'Пятница': 5,
    'Суббота': 6,
  }

  const dateObj = new Date();
  const currentWeekDay = dateObj.getDay();
  
  const weekDays = document.querySelectorAll('#week-day') //nodelist 

  weekDays.forEach( (day) => {
    if (weekDaysMap[day.textContent] === currentWeekDay){
      day.parentElement.classList.add('active-day') 
    }
  })
  

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
  
  return targetDate.toISOString().split('T')[0]; // Формат YYYY-MM-DD
}