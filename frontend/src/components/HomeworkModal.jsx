import { useEffect, useRef, useState } from "react"
import NotificationInner from "./notifications/NotificationInner"
import homeworkAPI from "../api/homeworkAPI"

const HomeworkModal = ({
  setShowDialog,
  lessonInfo,
  homeworkText,
  homeworkUpdated,
}) => {
  
  const [inputValue, setInputValue] = useState('')
  
  if (lessonInfo) {
    const {
      groupDataValue,
      dateDataValue,
      lessonIndex,
      lessonDay,
      lessonName,
    } = lessonInfo
    
    const [readOnly, setReadOnly] = useState(true)
    const textareaRef = useRef("")
    const dialogRef = useRef(null)
    
    
    const dialog = dialogRef.current
    
    if (dialog) {
      dialog.showModal() // Используем нативный метод
    }

    const isAdmin = true // ПОТОМ ПОМЕНЯТЬ

    useEffect(() => {
      if (isAdmin) {
        setReadOnly(false)
      }
    }, [])

    const handleTextInputClick = (event) => {
      event.preventDefault()
      event.target.focus()
    }

    const onInput = (event) => {
      setInputValue(event.target.value)
    }

    const handleHomeworkSubmit = (event) => {
      event.preventDefault()
      const homeworkText = inputValue
      console.log(
        "СОхраняем дз: ",
        groupDataValue,
        dateDataValue,
        lessonIndex,
        homeworkText
      )
      homeworkAPI.saveHomework(
        groupDataValue,
        dateDataValue,
        lessonIndex,
        homeworkText
      )
      dialog.close() // нативное закрытие (обязательно!!)
      setShowDialog(false) // просто убираем компонент из ScheduleContainer
    }

    const handleCancel = (event) => {
      event.preventDefault()
      textareaRef.current.value = ""
      dialog.close()  
      setShowDialog(false) 
    }

    const handleClickOutside = (e) => {
      if (dialog && e.target === dialog) {
        dialog.close() 
        setShowDialog(false) 
        textareaRef.current.value = ""
      }
    }

    //простой хук для решения проблемы из-за которой текст в поле ввода домашки не стирался
    useEffect(() => {
      if (homeworkText) {
        setInputValue(homeworkText)
        setTimeout(() => {
          homeworkText = ''
        }, 300)
      } else {
        setInputValue('')
      }
      
    }, [homeworkText])

    return (
      <dialog
        data-modal
        className="modal"
        ref={dialogRef}
        onClick={handleClickOutside}
      >
        <form id="homework-form" method="post" onSubmit={handleHomeworkSubmit}>
          <h3>
            <strong>{lessonName}</strong>, {lessonDay}
          </h3>
          <textarea 
            ref={textareaRef}
            value={inputValue}
            onClick={handleTextInputClick}
            onInput={onInput}
            name="text-input"
            id="text-input"
            placeholder={"введите домашнее задание..."}
            rows={6}
            readOnly={readOnly}
          />
          <p className="updated-at"></p>
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
}
export default HomeworkModal
