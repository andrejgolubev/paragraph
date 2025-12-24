import { useEffect, useRef, useState } from "react"
import NotificationInner from "./notifications/NotificationInner"
import homeworkAPI from "../api/homeworkAPI"

const HomeworkModal = ({
  showDialog,
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
      setInputValue(event.target.value.trim())
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
      dialog.close()
    }

    const handleCancel = (event) => {
      event.preventDefault()
      textareaRef.current.value = ""
      dialog.close()
    }

    const handleClickOutside = (e) => {
      if (dialog && e.target === dialog) {
        dialog.close()
        textareaRef.current.value = ""
      }
    }

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
          // className={homeworkText? 'dark' : ''}
            ref={textareaRef}
            // defaultValue={homeworkText}
            value={inputValue? inputValue: homeworkText}
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
