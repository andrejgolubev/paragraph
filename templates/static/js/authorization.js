const profileIcon = document.querySelector('.profile-icon')

profileIcon.addEventListener('click', () => {
    
})


function handleRegistrationSubmit(event) {
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


async function registerUser(username, password) {
  try {
    console.log('Registering user:', username); // БЕЗ ПАРОЛЯ!
    
    const response = await fetch(`http://127.0.0.1:8000/user/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password, // ТОЛЬКО В ТЕЛЕ ЗАПРОСА
      }),
    });
    
    if (response.ok) {
      showNotification("Регистрация успешна", "success");
      return await response.json();

    } else {
      const errorData = await response.json();
      showNotification(errorData.detail || "Ошибка регистрации", "error");
      return null;
    }
  } catch (error) {
    console.error("Registration error:", error);
    showNotification("Ошибка соединения", "error");
    return null;
  }
}