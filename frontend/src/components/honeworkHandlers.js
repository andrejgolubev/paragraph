// СТАРАЯ ФУНКЦИЯ (ДЛЯ ОЗНАКОМЛЕНИЯ)
// СТАРАЯ ФУНКЦИЯ (ДЛЯ ОЗНАКОМЛЕНИЯ)
// СТАРАЯ ФУНКЦИЯ (ДЛЯ ОЗНАКОМЛЕНИЯ)

function addHomeworkHandlers() {
  const homeworkButtons = document.querySelectorAll(".homework")

  console.log(`Found ${homeworkButtons.length} homework buttons`)

  homeworkButtons.forEach((hmwButton) => {
    hmwButton.addEventListener("click", function () {
      const lessonElement = hmwButton.parentElement
      const lessonName = lessonElement.querySelector(
        ".lesson-text strong"
      ).textContent
      const lessonText = lessonElement
        .querySelector(".lesson-text")
        .textContent.replace(lessonName, "")
        .split(",")
        .join(", ")
        
      const lessonIndex = lessonElement.parentElement.getAttribute("data-index")
      const lessonDay = lessonElement.parentElement.getAttribute("data-date") //x ноября , достается из колонки

      let formHeader = document.querySelector("#homework-form h3")
      formHeader.innerHTML = `<p><strong>${lessonName}</strong>, ${lessonDay}</p> <p>${lessonText}</p>`

      //реализация связи с эндпоинтом
      const groupDataValue = scheduleContainer.getAttribute("group-data-value")
      const dateDataValue = scheduleContainer.getAttribute("date-data-value")
      
      console.log("Homework button clicked. lessonInfo:", {
        groupDataValue,
        dateDataValue,
        lessonIndex,
      })

      const lessonInfo = {
        groupDataValue: groupDataValue,
        dateDataValue: dateDataValue,
        lessonIndex: parseInt(lessonIndex),
      }
      

    })
  })
}
