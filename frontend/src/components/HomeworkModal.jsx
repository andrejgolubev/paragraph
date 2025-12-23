import { useEffect, useRef, useState } from "react"
import NotificationInner from "./notifications/NotificationInner"
import homeworkAPI from "../api/homeworkAPI"

const HomeworkModal = ({ showDialog, lessonInfo }) => {
  // с lessonInfo обязательно достать информацию и разместить в модалке
  const isAdmin = true // ПОТОМ ПОМЕНЯТЬ

  if (lessonInfo) {
    console.log("lessonInfo from HomeworkModal :>> ", lessonInfo)
    const {
      groupDataValue,
      dateDataValue,
      lessonIndex,
      lessonDay,
      lessonName,
    } = lessonInfo

    console.log("lessonName :>> ", lessonName)
    const [readOnly, setReadOnly] = useState(true)
    const textareaRef = useRef("")
    const dialogRef = useRef(null)

    const dialog = dialogRef.current

    if (dialog && showDialog) {
      dialog.showModal() // Используем нативный метод
    }

    useEffect(() => {
      if (isAdmin) {
        setReadOnly(false)
      }
    }, [])

    const handleTextInputClick = (event) => {
      // event.preventDefault()
      event.target.focus()
    }

    const onInput = (event) => {
      const value = event.target.value.trim()
    }

    const handleHomeworkSubmit = (event) => {
      event.preventDefault()
    }

    const handleCancel = (event) => {
      event.preventDefault()
      dialog.close()
    }

    const handleClickOutside = (e) => {
      if (dialog && e.target === dialog) {
        dialog.close()
      }
    }

    return (
      <dialog
        data-modal
        className="modal"
        ref={dialogRef}
        onClick={handleClickOutside}
        // open={showDialog}
      >
        <form id="homework-form" method="post" onSubmit={handleHomeworkSubmit}>
          <h3><strong>{lessonName}</strong>, {lessonDay}</h3>
          <textarea
            ref={textareaRef}
            onClick={handleTextInputClick}
            onInput={onInput}
            name="text-input"
            id="text-input"
            placeholder="введите домашнее задание..."
            rows={6}
            readOnly={readOnly}
            defaultValue={""}
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
