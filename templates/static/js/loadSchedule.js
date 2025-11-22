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
              <div class="lesson-text">${escapeHtml(lesson.text)}</div>
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


  scheduleContainer.className = "schedule-container loaded";
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

