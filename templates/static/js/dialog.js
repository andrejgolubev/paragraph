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

  currentLessonInfo = lessonInfo;

  // Сбрасываем поле ввода перед открытием
  // if (textInput) {
  //   textInput.value = "";
  // }

  // Загружаем существующее ДЗ если есть
  loadExistingHomework(lessonInfo);

  modalElement.showModal();
}

// ✅ Функция для загрузки существующего ДЗ
async function loadExistingHomework(lessonInfo) {
  try {
    const { textInput } = getModalElements();

    if (!textInput) {
      console.error("Text input not found!");
      return;
    }

    const response = await fetch(
      `http://127.0.0.1:8000/homework/get?group_data_value=${lessonInfo.groupDataValue}&date_data_value=${lessonInfo.dateDataValue}&day_index=${lessonInfo.dayIndex}&time_slot_index=${lessonInfo.timeSlotIndex}&lesson_index=${lessonInfo.lessonIndex}`
    );

    if (response.ok) {
      const homeworkData = await response.json();
      textInput.value = homeworkData.homework || "";
    }
  } catch (error) {
    console.error("Error loading homework:", error);
  }
}

// ✅ Обработчик отправки формы
function handleHomeworkSubmit(event) {
  event.preventDefault();

  if (!currentLessonInfo) return;

  const { textInput } = getModalElements();

  if (!textInput) {
    console.error("Text input not found!");
    return;
  }

  const homeworkText = textInput.value.trim();
  saveHomework(currentLessonInfo, homeworkText);
}

// ✅ Функция сохранения ДЗ
async function saveHomework(lessonInfo, homeworkText) {
  try {
    const response = await fetch("http://127.0.0.1:8000/homework/save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        group_data_value: lessonInfo.groupDataValue,
        date_data_value: lessonInfo.dateDataValue,
        day_index: lessonInfo.dayIndex,
        homework: homeworkText,
      }),
    });

    if (response.ok) {
      console.log("Homework saved successfully");
      const { modalElement } = getModalElements();

      if (modalElement) {
        modalElement.close();
      }

      showNotification("Домашнее задание сохранено", "success");
    }
  } catch (error) {
    console.error("Error saving homework:", error);
    showNotification("Ошибка сохранения", "error");
  }
}

// ✅ Обработчик отмены
function handleCancel() {
  const { modalElement } = getModalElements();

  if (modalElement) {
    modalElement.close();
  }
}

// ✅ Инициализация после загрузки DOM
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
  const notification = document.createElement("div");
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 6px;
    color: white;
    z-index: 1000;
    background: ${type === "success" ? "#28a745" : "#dc3545"};
  `;
  notification.textContent = message;

  document.body.appendChild(notification);

  setTimeout(() => {
    document.body.removeChild(notification);
  }, 3000);
}


document.addEventListener("DOMContentLoaded", initHomeworkModal);

export { openHomeworkModal, initHomeworkModal };
