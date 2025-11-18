async function loadDates() {
  const response = await fetch("http://127.0.0.1:8000/schedule/get-all-dates");
  return response.json(); // возвращаем json а не сырой response
}

const selectInput = document.getElementById("select-input");
const datesList = document.getElementById("dates");
const selectBody = document.querySelector(".select-block__body");

const dates = await loadDates();

// dates.forEach( (element) => {
//   console.log(element)
// });

dates.slice(-10).forEach((date) => {
  const li = document.createElement("li");
  const link = document.createElement("a");

  link.textContent = date.date;
  link.href = "#"; 

  // Обработчик выбора даты
  link.addEventListener("click", (event) => {
    event.preventDefault(); 
    selectInput.value = date.date; 
    selectBody.classList.remove("active-search");
  });
  
  li.appendChild(link);
  datesList.appendChild(li);
});

selectInput.addEventListener("click", (event) => {
  console.log('click on button'); // добавил логи но они не выводятся даже
  
  event.stopPropagation();
  event.target.toggle("active-search");
});

document.addEventListener("click", (event) => {
  if (!selectBody.contains(event.target)) {
    selectBody.classList.remove("active-search");
  }
});

selectInput.addEventListener("focus", () => {
  selectBody.classList.add("active-search");
});