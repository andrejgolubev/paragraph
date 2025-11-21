

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
  const tipElem = document.querySelector('.tip')
  const scheduleContainer = 
  document.getElementById("schedule-container");
  scheduleContainer.className = 'schedule-container loading';

  let html = `
    <div class="schedule-header">
      ${
        scheduleData.group_data_value
          ? `<p>Группа: ${scheduleData.group_data_value}</p>`
          : ""
      }
      ${
        scheduleData.date_data_value
          ? `<p>Дата: ${scheduleData.date_data_value}</p>`
          : ""
      }
    </div>
  `;

  // Проверяем что данные есть
  if (!scheduleData.days || !scheduleData.schedule) {
    scheduleContainer.innerHTML =
      html + `<p class="error">Нет данных расписания</p>`;
    return;
  }

  html += `
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
        <p>${day.day}</p>
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
          let lessonId = 'default'
          if (lesson.type === 'Лек.'){ 
            lessonId = 'lec' 
          } else if (lesson.type === 'Упр.'){
            lessonId = 'upr'
          } else if (lesson.type === 'Лаб.'){
            lessonId = 'lab'
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
              <div class="lesson-text">${lesson.text}</div>
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
  tipElem.classList.remove('tip-active')
  setTimeout(() => {
    scheduleContainer.className = 'schedule-container loaded';
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

function formatLessonText(text) {
  // Добавляем переносы строк для лучшего отображения
  return text.replace(/,/g, ",<br>");
}
