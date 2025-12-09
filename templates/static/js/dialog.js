let currentLessonInfo = null;
let modalElement = null;
let textInput = null;

// Функция для безопасного получения элементов
function getModalElements() {
  if (!modalElement) {
    modalElement = document.querySelector(".modal");
  }
  if (!textInput) {
    textInput = document.getElementById("text-input");
  }
  return { modalElement, textInput };
}

// Функция для открытия модального окна
function openHomeworkModal(lessonInfo) {
  const { modalElement, textInput } = getModalElements();
  
  if (!modalElement) {
    console.error("Modal element not found!");
    return;
  }

  currentLessonInfo = lessonInfo
  // Сбрасываем поле ввода перед открытием
  if (textInput){
    textInput.value = ""
  }

  // Загружаем существующее ДЗ если есть
  displayHomework(currentLessonInfo);

  modalElement.showModal();
}




// Функция сохранения ДЗ
async function saveHomework(lessonInfo, homeworkText) {
  if (!homeworkText) {
    showNotification('д/з не может быть пустым :(')
    return 
  }
  if (homeworkText.length < 5){
    showNotification('д/з не может быть таким коротким.')
    return 
  }
  console.log('saveHomework. lessonInfo: ', lessonInfo)
  const {groupDataValue, dateDataValue, lessonIndex} = lessonInfo
  try {
    const response = await fetch(
       `http://127.0.0.1:8000/homework/save?group_data_value=${groupDataValue}&date_data_value=${dateDataValue}&lesson_index=${lessonIndex}&homework=${homeworkText}`, 
       {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        group_data_value: groupDataValue,
        date_data_value: dateDataValue,
        lesson_index: lessonIndex,
        homework: homeworkText,
      }),
    });
    
    if (response.ok) {
      showNotification("Домашнее задание сохранено", "success");

      const { modalElement } = getModalElements();
      
      if (modalElement) {
        modalElement.close();
      }
      
    }
    else {
      const errorData = await response.json();
      showNotification(`${errorData.detail || "произошла неизвестная ошибка"}`, "error");
      // Или показываем ошибку в форме:
      // showFormError(errorData.detail || "Ошибка сохранения");
    }
  } catch (error) {
    console.error("Error saving homework:", error);
    showNotification("Ошибка сохранения", "error");
  }
}

async function displayHomework(lessonInfo) {
  const {groupDataValue, dateDataValue, lessonIndex} = lessonInfo
  const response = await fetch(`http://127.0.0.1:8000/homework/get?group_data_value=${groupDataValue}&date_data_value=${dateDataValue}&lesson_index=${lessonIndex}`)
  const hmwText = await response.json()
  console.log(hmwText)

  const { modalElement, textInput } = getModalElements();

  textInput['value'] = hmwText.homework
}

// await displayHomework('1633', '2025-11-03', '2')


// Обработчик отправки формы
function handleHomeworkSubmit(event) {
  event.preventDefault();

  if (!currentLessonInfo) return;

  const { textInput } = getModalElements();
  if (!textInput) {
    console.error("Text input not found!");
    return;
  }

  const homeworkText = textInput.value.trim();
  console.log('homework submit debugging. currentLessonInfo: ', currentLessonInfo, 'homeworkText', homeworkText)
  saveHomework(currentLessonInfo, homeworkText);
}

// Обработчик отмены
function handleCancel() {
  const { modalElement } = getModalElements();
  
  if (modalElement) {
    modalElement.close();
  }
}

// Инициализация после загрузки DOM
function initHomeworkModal() {
  const { modalElement } = getModalElements();
  const homeworkForm = document.getElementById("homework-form");
  const cancelButton = document.querySelector(".btn-cancel");
  
  
  
  if (!modalElement) {
    console.error("Modal element not found during initialization!");
    return;
  }

  // Обработчик клика на backdrop
  const handleModalClick = ({ currentTarget, target }) => {
    const isClickedOnBackdrop = target === currentTarget;
    if (isClickedOnBackdrop) {
      currentTarget.close();
    }
  };

  modalElement.addEventListener("click", handleModalClick);
  


  // Обработчик отправки формы
  if (homeworkForm) {
    homeworkForm.addEventListener("submit", handleHomeworkSubmit);
  }

  // Обработчик кнопки отмены
  if (cancelButton) {
    cancelButton.addEventListener("click", handleCancel);
  }

  console.log("Homework modal initialized successfully");
}

// ✅ Функция для показа уведомлений
function showNotification(message, type = "info") {
  // Можно заменить на более красивую реализацию
  const notification = document.querySelector('.notification')
  notification.className = `notification ${type}`;
  notification.textContent = message;
  
  notification.style.cssText = `
  background: ${type === "success" ? "#28a745" : "#dc3545"};
  `;
  
  notification.classList.add('active')
  notification.classList.add(type)

  setTimeout(() => {
    notification.classList.remove('active');
  }, 3000);
}


document.addEventListener("DOMContentLoaded", initHomeworkModal);

export { openHomeworkModal, initHomeworkModal };
