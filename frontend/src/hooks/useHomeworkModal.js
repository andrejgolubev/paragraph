

//ЭТА ФУНКЦИЯ ИСП. ДЛЯ СКРЕПОЧЕК (onClick={onClickOpenHomeworkModal} для каждой) 
  const onClickOpenHomeworkModal = (lessonInfo) => {
    // будем потом в lessonInfo в FASTAPI передавать роль юзера, чтобы readonly убирался опицонально
    const [showDialog, setShowDialog] = useState(false)

    // Загружаем существующее ДЗ если есть
    displayHomework(lessonInfo)

    setShowDialog(true)
  }

