import { loadSchedule } from "./loadSchedule.js";

const tipElem = document.querySelector(".tip");

if (tipElem) {
  setTimeout(() => {
    tipElem.classList.add("active");
    console.log("tipElem :>> ", tipElem);
    // Проверяем стили после добавления класса
  }, 400);
}
