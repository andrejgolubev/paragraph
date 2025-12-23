import { useEffect, useRef, useState } from "react"
import NotificationInner from './notifications/NotificationInner'

const HomeworkModal = () => {
  
  const isAdmin = true // ПОТОМ ПОМЕНЯТЬ 

  const [readOnly, setReadOnly] = useState(true)
  const textareaRef = useRef(null)

  //НАЧАЛАСЬ ФУНКЦИЯ И USESTATE ИСП. ДЛЯ СКРЕПОЧЕК
  const [showDialog, setShowDialog] = useState(false)

  const onClickOpenHomeworkModal = (lessonInfo) => {
    // будем потом в lessonInfo в FASTAPI передавать роль юзера, чтобы readonly убирался опицонально

    // Загружаем существующее ДЗ если есть
    displayHomework(lessonInfo)

    setShowDialog(true)
  } 
  //КОНЧИЛАСЬ ФУНКЦИЯ И USESTATE ИСП. ДЛЯ СКРЕПОЧЕК


  useEffect( () => {
    if (isAdmin) {
      setReadOnly(false)
    }
  }, []) 

  const handleTextInputClick = (event) => {
    event.target.focus()
  }

  const onInput = (event) => {
    const value = event.target.value.trim() 
  }


  const handleHomeworkSubmit = (event) => {
    event.preventDefault()
    const homeworkText = textInput.value.trim()
    
  }

  const handleCancel = (event) => { 
    event.preventDefault()
    setShowDialog((prev) => !prev) 
  } 

  return (
    <dialog data-modal className="modal" open={!showDialog}>
      <form id="homework-form" method="post" onSubmit={handleHomeworkSubmit}>
        <h3>домашнее задание</h3>
        <textarea
          ref={textareaRef}
          onClick={handleTextInputClick}
          onInput={onInput}
          name="text-input"
          id="text-input"
          placeholder="введите домашнее задание..."
          rows={6}
          readOnly = {readOnly} 
          defaultValue={""}
        />
        <p className="updated-at" />
        <div className="modal-buttons">
          <button type="button" className="btn-cancel" onClick={handleCancel}>
            отмена
          </button>
          <NotificationInner />
          <button type="submit" className="btn-save">
            сохранить
          </button>
        </div>
      </form>
    </dialog>
  )
}

export default HomeworkModal
