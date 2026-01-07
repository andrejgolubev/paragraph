import { useContext, useEffect, useRef, useState } from "react"
import NotificationInner from "./notifications/NotificationInner"
import homeworkAPI from "../api/homeworkAPI"
import { Context } from "../context/Provider"
import { convertDate } from "../utils/converters"
import { useWindowSize } from "../hooks/useWindowSize"
import { useModeratedGroups } from "../hooks/useModeratedGroups"

const HomeworkModal = ({
  // showDialog,
  setShowDialog,
  lessonInfo,
  homeworkText,
  homeworkUpdated,
}) => {
  const {darkTheme} = useContext(Context)
  const {width} = useWindowSize()

  const {setNotificationOuterActive, setNotificationOuterMessage, userRole, username } = useContext(Context)
  const [inputValue, setInputValue] = useState("")
  const [notificationInnerActive, setNotificationInnerActive] = useState(false)
  const [lastUpdate, setLastUpdate] = useState("")
  const showErrorTimerRef = useRef(null)

  const showError = () => {
    setNotificationInnerActive(true)
    
    setTimeout(() => {
      setNotificationInnerActive(false)
    }, 3100) // 3100 a не 3000 чтобы локальный isActive сработал и плавно ушла кнопка 

  }

  if (lessonInfo) {
    const {
      groupDataValue,
      dateDataValue,
      lessonIndex,
      lessonDay,
      lessonName,
    } = lessonInfo

    const [respText, setRespText] = useState(
      // 'д/з не может быть пустым' 
      'недостаточно прав для управления этим д/з'
    )

    const [readOnly , setReadOnly] = useState(false) 

    const textareaRef = useRef("")
    const dialogRef = useRef(null)
    const dialog = dialogRef.current  

    // срабатывает тогда когда модалка появляется
    useEffect(() => {
      if (dialog) {
        if (!homeworkUpdated) {
          setLastUpdate("")
        } else {

          const hmwUpdatedTime = homeworkUpdated.split("T")
          const hmwDate = convertDate(hmwUpdatedTime[0])
          const hmwTime = hmwUpdatedTime[1].slice(0, 5)
  
          setLastUpdate("последнее изменение: " + hmwDate + ", " + hmwTime)
        }
        
        dialog.showModal() // используем нативный метод
      
        return () => {
          dialog.close()
          homeworkText = ""
        }
      }
    }, [dialog, homeworkUpdated])


    const { moderatedGroups } = useModeratedGroups()

    useEffect( () => {
      homeworkAPI.convertFromDataValue({groupDataValue}).then( (resp) => {
        const currentGroupNumber = resp?.group_number
        if (moderatedGroups.some( num => num === currentGroupNumber )) {
          setReadOnly(false)
        } else { 
          setReadOnly(true)
        }
      })

      return () => setReadOnly(true)

    }, [moderatedGroups])


    const handleTextInputClick = (event) => {
      event.target.focus()
    }

    const onInput = (event) => {
      setInputValue(event.target.value)
    }

    const handleHomeworkSubmit = (event) => {
      event.preventDefault()
     
      const homeworkTextClean = inputValue.trim()

      homeworkAPI.saveHomework(
        groupDataValue,
        dateDataValue,
        lessonIndex,
        homeworkTextClean
      ).then( resp => {
        if (!(resp.detail === 'saved')) {
          setRespText(resp.detail)
          console.log('resp.detail из handleHomeworkSubmit:>> ', resp.detail);
          showError()
          return
        } else { 
          // если сохранена домашка, то:
          setShowDialog(false) // просто убираем компонент из ScheduleContainer
          
          setLastUpdate('')
          setNotificationOuterMessage('домашнее задание сохранено.')
          setNotificationOuterActive(true)
        }
      })

      
      if (!homeworkTextClean) {
        setRespText('д/з не может быть пустым')
        showError()
        return
      }
    }

    const handleCancel = (event) => {
      event.preventDefault()
      textareaRef.current.value = ""
      setShowDialog(false)
    }

    const handleClickOutside = (e) => {
      if (dialog && e.target === dialog) {
        textareaRef.current.value = ""
        setShowDialog(false)
      }
    }

    //простой хук для решения проблемы из-за которой текст в поле ввода домашки не стирался
    useEffect(() => {
      if (homeworkText) {
        setInputValue(homeworkText)
        // для того чтобы текст в поле ввода домашки уже был пуст после закрытия модалки есть useEffect в котором мы закрываем модалку
      } else {
        setInputValue("")
      }
    }, [homeworkText])


    return (
      <dialog
        data-modal
        className={`modal ${darkTheme? 'dark' : ''}`}
        ref={dialogRef}
        onClick={handleClickOutside}
        onCancel={handleCancel}
      >
        <form id="homework-form" method="post" onSubmit={handleHomeworkSubmit}>
          <h3>
            <p><strong>{lessonName}</strong>, {lessonDay}</p>
          </h3>
          <textarea
            ref={textareaRef}
            value={inputValue}
            onPointerDown={handleTextInputClick}
            onClick={handleTextInputClick}
            onInput={onInput}
            name="text-input"
            id="text-input"
            placeholder={readOnly? "домашнее задание пока ещё никто не добавил..." : "введите домашнее задание..."}
            rows={6}
            readOnly={readOnly}
          />
          <p className="updated-at">{homeworkText && lastUpdate}</p>
          <div className="modal-buttons">
            {/* если мобилка то рендерим кнопку "сохранить" перед нотификэйшном  */}
            {width > 800 ? (
                <>
                  <button type="button" className="btn-cancel" onClick={handleCancel}>
                    отмена
                  </button>
                  <NotificationInner
                    message={respText}
                    type={"error"}
                    notificationInnerActive={notificationInnerActive}
                    setNotificationInnerActive={setNotificationInnerActive}
                  /> 
                  <button type="submit" className={`btn-${readOnly? 'cancel' : 'save'}`}>
                    сохранить
                  </button>
                </>
            ) : (
              <>
                <button type="submit" className={`btn-${readOnly? 'cancel' : 'save'}`}>
                  сохранить
                </button>
                <button type="button" className="btn-cancel" onClick={handleCancel}>
                  отмена
                </button>
                {notificationInnerActive && 
                (<NotificationInner
                  message={respText}
                  type={"error"}
                  notificationInnerActive={notificationInnerActive}
                  setNotificationInnerActive={setNotificationInnerActive}
                /> )
                }
              </>
            )
              }
          </div>
        </form>
      </dialog>
    )
  }
}
export default HomeworkModal
