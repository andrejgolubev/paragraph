// // Функция для выбора группы
// async function selectGroup(groupDataValue) {
//     try {
//         const response = await fetch('/schedule/select-group', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ group_data_value: groupDataValue })
//         });
        
//         if (response.ok) {
//             // После успешного сохранения группы, загружаем расписание
//             await loadSchedule(groupDataValue);
//         }
//     } catch (error) {
//         console.error('Error selecting group:', error);
//     }
// }

// // Функция для загрузки расписания
// async function loadSchedule(groupDataValue, dateDataValue = null) {
//     try {
//         const params = new URLSearchParams({
//             group_data_value: groupDataValue
//         });
        
//         if (dateDataValue) {
//             params.append('date_data_value', dateDataValue);
//         }
        
//         const response = await fetch(`/schedule/get-schedule?${params}`);
//         const scheduleData = await response.json();
        
//         // Отображаем расписание на странице
//         displaySchedule(scheduleData);
//     } catch (error) {
//         console.error('Error loading schedule:', error);
//     }
// }

// // Функция для отображения расписания
// function displaySchedule(scheduleData) {
//     const scheduleContainer = document.getElementById('schedule-container');
//     // Здесь твоя логика отображения расписания
//     scheduleContainer.innerHTML = JSON.stringify(scheduleData, null, 2);
// }

// // При загрузке страницы проверяем сохраненную группу
// document.addEventListener('DOMContentLoaded', function() {
//     // Можно также попробовать загрузить расписание если есть cookie
//     // или ждать пока пользователь выберет группу
// });

// // Функция для загрузки расписания по выбранным значениям
// async function loadScheduleFromSelected() {
//     const groupSelect = document.getElementById('group-select');
//     const dateSelect = document.getElementById('date-select');
    
//     if (groupSelect.value && dateSelect.value) {
//         await loadSchedule(groupSelect.value, dateSelect.value);
//     }
// }

// // При загрузке страницы пытаемся загрузить расписание если есть сохраненная группа
// document.addEventListener('DOMContentLoaded', async function() {
//     // Можно попробовать получить группу из cookie через API
//     try {
//         const response = await fetch('/schedule/get-schedule');
//         if (response.ok) {
//             const scheduleData = await response.json();
//             displaySchedule(scheduleData);
//         }
//     } catch (error) {
//         // Если нет сохраненной группы - ничего не делаем
//     }
// });