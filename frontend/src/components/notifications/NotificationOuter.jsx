import { useEffect } from "react"
import { useUiStore } from "../../store/uiStore"


const NotificationOuter = () => {
  const {
    notificationOuterActive,
    setNotificationOuterActive,
    notificationOuterMessage,
    notificationOuterType,
  } = useUiStore()
  
  useEffect(() => {
    const timer = setTimeout( async () => {
      setNotificationOuterActive(false)
    }, 3000)

    return () => clearTimeout(timer) //отменяем ожидание если элемент notification inner больше не вмонтирован в разметку 
  }, [notificationOuterActive])


  useEffect(() => {
    return () => setNotificationOuterActive(false) // если компонент размонтирован, скрываем его
  }, [])

  return (
    <div
      className={`notification outer ${
        notificationOuterActive ? "active" : ""
      } ${notificationOuterType}`}
    >
      {notificationOuterMessage}
    </div>
  )
}

export default NotificationOuter
