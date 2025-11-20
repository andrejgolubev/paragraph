import {loadSchedule} from './loadSchedule.js'

document.addEventListener('DOMContentLoaded', function() {
  const tipElem = document.querySelector(".tip");

  if (tipElem) {
    setTimeout(() => {
      tipElem.classList.add("tip-active");
      
      // Проверяем стили после добавления класса
    }, 1000);
  }
});