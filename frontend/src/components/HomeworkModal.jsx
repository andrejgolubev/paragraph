import { useContext, useEffect, useRef, useState } from "react"
import NotificationInner from "./notifications/NotificationInner"
import homeworkAPI from "../api/homeworkAPI"
import { Context } from "../context/Provider"
import { convertDate } from "../utils/converters"

const HomeworkModal = ({
  setShowDialog,
  lessonInfo,
  homeworkText,
  homeworkUpdated,
}) => {
  const { notificationOuterActive, setNotificationOuterActive, notificationOuterMessage, setNotificationOuterMessage,  } = useContext(Context)
  const [inputValue, setInputValue] = useState("")
  const [noTextSubmitError, setNoTextSubmitError] = useState(false)
  const [lastUpdate, setLastUpdate] = useState("")

  if (lessonInfo) {
    const {
      groupDataValue,
      dateDataValue,
      lessonIndex,
      lessonDay,
      lessonName,
    } = lessonInfo

    const [readOnly, setReadOnly] = useState(true)
    const [respText, setRespText] = useState('д/з не может быть пустым')
    const textareaRef = useRef("")
    const dialogRef = useRef(null)
    
    const dialog = dialogRef.current

    // срабатывает тогда когда модалка появляется
    useEffect(() => {
      if (dialog) {
        if (!homeworkUpdated) {
          setLastUpdate("")
        } else {

          let hmwUpdated = homeworkUpdated.split("T")
          let hmwDate = convertDate(hmwUpdated[0])
          let hmwTime = hmwUpdated[1].slice(0, 5)
  
  
          setLastUpdate("последнее изменение: " + hmwDate + ", " + hmwTime)
          console.log("lastUpdate :>> ", lastUpdate)
        }
        
        dialog.showModal() // используем нативный метод
      }
    }, [dialog, homeworkUpdated])


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
      const homeworkTextClean = inputValue.trim()
      if (!homeworkTextClean) {
        setNoTextSubmitError(true)
        return
      }


      homeworkAPI.saveHomework(
        groupDataValue,
        dateDataValue,
        lessonIndex,
        homeworkTextClean
      ).then( resp => {
        console.log('response from hmwModal :>> ', resp)
        console.log('response.detail from hmwModal :>> ', resp.detail)

        if (!(resp.detail === 'saved')) {
          setRespText(resp.detail)
          setNoTextSubmitError(true)
        } else { 
          // если сохранена домашка, то:
          dialog.close() // нативное закрытие (обязательно!!)
          setShowDialog(false) // просто убираем компонент из ScheduleContainer
          setLastUpdate('')
          
          setNotificationOuterMessage('домашнее задание сохранено.')
          setNotificationOuterActive(true)
        }
      })

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
        setTimeout( async () => {
          homeworkText = ""
        }, 300)
      } else {
        setInputValue("")
      }
    }, [homeworkText])



    return (
      <dialog
        data-modal
        className="modal"
        ref={dialogRef}
        onClick={handleClickOutside}
        onCancel={handleCancel}
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
          <p className="updated-at">{homeworkText && lastUpdate}</p>
          <div className="modal-buttons">
            <button type="button" className="btn-cancel" onClick={handleCancel}>
              отмена
            </button>
            <NotificationInner
              message={respText}
              type={"error"}
              noTextSubmitError={noTextSubmitError}
              setNoTextSubmitError={setNoTextSubmitError}
            />
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
