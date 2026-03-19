import { useEffect } from "react"
import { useUiStore } from "../../store/uiStore"


const NotificationOuter = () => {
  const {
    notificationOuterActive,
    setNotificationOuterActive,
    notificationOuterMessage,
    notificationOuterType,
    notificationOuterIsLeft,
  } = useUiStore()
  
  useEffect(() => {
    const timer = setTimeout( async () => {
      setNotificationOuterActive(false)
    }, 3000)

    return () => clearTimeout(timer) //отменяем ожидание если элемент notification inner больше не вмонтирован в разметку 
  }, [notificationOuterActive, setNotificationOuterActive])


  useEffect(() => {
    return () => setNotificationOuterActive(false) // если компонент размонтирован, скрываем его
  }, [setNotificationOuterActive])

  return (
    <div
      className={`notification outer 
      ${ notificationOuterActive ? "active" : ""} 
      ${ notificationOuterIsLeft ? "from-left" : ""}
      ${ notificationOuterType }`}
    >
      {notificationOuterMessage}
    </div>
  )
}

export default NotificationOuter
