import { useEffect, useRef, useState } from "react"
import NotificationInner from "../notifications/NotificationInner"
import API, {showNotificationOuter}  from "../../api/API"
import { convertDate } from "../../utils/converters"
import { useWindowSize } from "../../hooks/useWindowSize"
import { useModeratedGroups } from "../../hooks/useModeratedGroups"
import { useThemeStore } from "../../store/themeStore"


const HomeworkModal = ({
  setShowDialog,
  lessonInfo,
  homeworkText,
  homeworkUpdated,
  homeworkAuthor, 
  homeworkExistsMap
}) => {
  const {
    groupDataValue,
    dateDataValue,
    lessonIndex,
    lessonDate,
    lessonName,
  } = lessonInfo

  const { width } = useWindowSize()
  const [inputValue, setInputValue] = useState("")
  const [lastUpdate, setLastUpdate] = useState("")
  const [notificationInnerActive, setNotificationInnerActive] = useState(false)
  const [notificationInnerMessage, setNotificationInnerMessage] = useState(
    "недостаточно прав для управления этим д/з"
  )
  const { darkTheme, notesEnabled } = useThemeStore()
  const [isReadOnly , setIsReadOnly] = useState(true) 
  const { moderatedGroups } = useModeratedGroups()

  useEffect( () => {
    setIsReadOnly(!notesEnabled)
  }, [isReadOnly, notesEnabled]) 

  const showNotificationInner = (msg) => {
    setNotificationInnerMessage(msg)
    setNotificationInnerActive(true)
    
    setTimeout(() => {
      setNotificationInnerActive(false)
    }, 3100) // 3100 a не 3000 чтобы локальный isActive сработал и плавно ушла кнопка 
  }

    
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

        setLastUpdate(
          "последнее изменение: " + hmwDate + ", " + hmwTime + 
          ` (изменено: ${homeworkAuthor})`
        )
      }
      dialog.showModal() // используем нативный метод
      return () => {
        dialog.close()
        setIsReadOnly(true)
        // eslint-disable-next-line react-hooks/exhaustive-deps 
        homeworkText = ""
        // игнорим линтер т.к. homeworkText не надо хранить при ре-рендерах
      }
    }
  }, [dialog, homeworkUpdated])


  useEffect( () => {
    if (notesEnabled) return  

    API.convertFromDataValue({groupDataValue}).then( (resp) => {
      const currentGroupNumber = resp?.group_number
      if (moderatedGroups.some( num => num === currentGroupNumber )) {
        setIsReadOnly(false)
      } else { 
        setIsReadOnly(true)
      }
    })
    return () => setIsReadOnly(true)
  }, [moderatedGroups, groupDataValue])


  const handleTextAreaClick = (event) => {
    setNotificationInnerActive(false) 
    event.target.focus()
  }

  const onInput = (event) => {
    setInputValue(event.target.value)
  }

  const handleHomeworkSubmit = (event) => {
    event.preventDefault()
    const homeworkTextClean = inputValue.trim()

    API.saveHomework(
      groupDataValue,
      dateDataValue,
      lessonIndex,
      homeworkTextClean
    ).then( resp => {
      if (!(resp.detail === 'saved')) { // FastAPI возвращает 'saved' если домашка сохранена успешно
        showNotificationInner(resp.detail)
        return
      } else { 
        // если сохранена домашка, то:
        setShowDialog(false) // просто убираем компонент из ScheduleContainer
        setLastUpdate('')
        homeworkExistsMap[lessonIndex] = true
        showNotificationOuter(resp.message , 'success')
      }
    })
  }

  const handleCancel = (event) => {
    event.preventDefault()
    setInputValue('')
    setShowDialog(false)
  }

  const handleClickOutside = (e) => {
    if (dialog && e.target === dialog) {
      setInputValue('')
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
          <p><strong>{lessonName}</strong>, {lessonDate}</p>
        </h3>
        <textarea
          value={inputValue}
          onClick={handleTextAreaClick}
          onInput={onInput}
          name="text-input"
          id="text-input"
          placeholder={
            notesEnabled ? 
              "добавьте заметку..."
            : isReadOnly 
              ? "домашнее задание пока ещё никто не добавил..." 
              : "введите домашнее задание..."
          }
          rows={6}
          readOnly={notesEnabled ? false : isReadOnly}
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
                  notificationInnerMessage={notificationInnerMessage}
                  notificationInnerActive={notificationInnerActive}
                  setNotificationInnerActive={setNotificationInnerActive}
                /> 
                <button type="submit" className={`btn-${isReadOnly? 'cancel' : 'save'}`}>
                  сохранить
                </button>
              </>
          ) : (
            <>
              <button type="submit" className={`btn-${isReadOnly? 'cancel' : 'save'}`}>
                сохранить
              </button>
              <button type="button" className="btn-cancel" onClick={handleCancel}>
                отмена
              </button>
              {notificationInnerActive && 
              (<NotificationInner
                notificationInnerMessage={notificationInnerMessage}
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
export default HomeworkModal
