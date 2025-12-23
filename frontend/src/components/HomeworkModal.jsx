import { useEffect, useRef, useState } from "react"
import NotificationInner from "./notifications/NotificationInner"

const HomeworkModal = (props) => {
  // с lessonInfo обязательно достать информацию и разместить в модалке
  const { lessonInfo, showDialog, setShowDialog } = props
  const isAdmin = true // ПОТОМ ПОМЕНЯТЬ

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
        <h3>домашнее задание</h3>
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
