document.addEventListener('DOMContentLoaded', function() {
  const tipElem = document.querySelector(".tip");
  console.log('Tip element:', tipElem);
  
  // Проверяем текущие стили
  console.log('Computed opacity:', window.getComputedStyle(tipElem).opacity);
  console.log('Computed display:', window.getComputedStyle(tipElem).display);
  console.log('Computed visibility:', window.getComputedStyle(tipElem).visibility);
  
  if (tipElem) {
    setTimeout(() => {
      console.log('Adding tip-active class');
      tipElem.classList.add("tip-active");
      
      // Проверяем стили после добавления класса
      setTimeout(() => {
        console.log('After adding class - opacity:', window.getComputedStyle(tipElem).opacity);
        console.log('Class list:', tipElem.classList);
      }, 100);
    }, 500);
  }
});