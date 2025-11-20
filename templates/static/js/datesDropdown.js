import {loadSchedule} from './loadSchedule.js'

let selectedGroupDataValue = null

const selectInput = document.getElementById("select-input");
const datesList = document.getElementById("dates");
const selectBody = document.querySelector(".select-block__body");


async function loadDates() {
  try {
    const response = await fetch("http://127.0.0.1:8000/schedule/get-all-dates");
    return response.json();
  } catch (error) {
    console.error("Error loading dates:", error);
    return [];
  }
}

// Функция для выбора даты (опционально)
async function selectDate(dateDataValue, dateText) {
  if (selectedGroupDataValue) {
    // Обновляем поле ввода даты и закрываем список дат
    selectInput.value = dateText; 
    selectBody.classList.remove("active-search"); 
    // Загружаем расписание
    await loadSchedule(selectedGroupDataValue, dateDataValue);
  }
}


const dates = await loadDates();


dates.slice(-10).forEach((date) => {
  const li = document.createElement("li");
  const link = document.createElement("a");

  link.textContent = date.date;
  link.href = "#"; 

  // Обработчик выбора даты
  link.addEventListener("click", async (event) => {
    event.preventDefault(); 
    await selectDate(date.data_value, date.date)
  });
  
  li.appendChild(link);
  datesList.appendChild(li);
});

selectInput.addEventListener("click", (event) => {
  if (!selectedGroupDataValue) {}

  event.stopPropagation();
  event.target.toggle("active-search");
});


document.addEventListener("click", (event) => {
  if (!selectBody.contains(event.target)) {
    selectBody.classList.remove("active-search");
  }
});



