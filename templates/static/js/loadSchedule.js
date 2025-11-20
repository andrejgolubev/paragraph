
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
  const scheduleContainer = document.getElementById("schedule-container");

  // Проверяем структуру данных
  console.log("Schedule data structure:", scheduleData);

  if (scheduleData.error) {
    scheduleContainer.innerHTML = `<p class="error">Ошибка: ${scheduleData.error}</p>`;
    return;
  }

  // Извлекаем расписание
  //   const schedule = scheduleData.schedule_data || scheduleData;
  const schedule = scheduleData;

  let html = `
    <div class="schedule-header">
      <h3>📅 Расписание</h3>
      ${
        scheduleData.group_data_value
          ? `<p>Группа: ${scheduleData.group_data_value}</p>`
          : ""
      }
      ${
        scheduleData.date_data_value
          ? `<p>Дата: ${scheduleData.date_data_value}</p>`
          : "<p>Текущая неделя</p>"
      }
    </div>
  `;

  if (!schedule.days || !schedule.schedule) {
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
  schedule.days.forEach((day) => {
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
  schedule.schedule.forEach((timeSlot) => {
    html += `
      <tr>
        <td>
          <p>${timeSlot.time_start}</p>
          <p>${timeSlot.time_end}</p>
        </td>
    `;

    // Занятия для каждого дня
    timeSlot.lessons.forEach((dayLessons) => {
      html += `<td>`;

      if (dayLessons.length > 0) {
        dayLessons.forEach((lesson) => {
          html += `
            <div class="lesson-item">
              ${
                lesson.type
                  ? `<span class="lesson-type">${lesson.type}</span>`
                  : ""
              }
              <div class="lesson-text">${lesson.text || ""}</div>
            </div>
          `;
        });
      } else {
        html += `<div class="lesson-empty">—</div>`;
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
}
