// СООБЩЕНИЕ ЕСЛИ ПО ЗАПРОСУ НИЧЕГО НЕ НАЙДЕНО (для групп и дат)
// ВСЯ ВЕСРТКА id=schedule-container меняется на верстку ошибки (СМОТРИ РЕАЛИЗАЦИЮ В groupsDropdown.js). РЕШЕНИЯ:
// 1. В App.jsx КОГДЖА НАПИШУ SCHEDULE-CONTAINER Schedule-container ?? HomepageError

const HomepageError = (props) => {
  const {
    inputValue,
    detail = "убедитесь в правильности написания и повторите попытку",
  } = props

  const scheduleContainer = document.getElementById("schedule-container")
  const tipElem = document.querySelector(".tip")
  tipElem.classList.remove("tip-active")

  setTimeout(() => {
    tipElem.classList.add("tip-active")
    scheduleContainer.innerHTML = ""
    // Проверяем стили после добавления класса
  }, 3000)

  return (
    
    <div class="error-message">
      <p>
        по запросу <strong>{inputValue}</strong> информацией пока не
        располагаю :(
      </p>
      <p>${detail}</p>
    </div>
    
  )
}

export default HomepageError
