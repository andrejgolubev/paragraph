import { useEffect } from "react"

const NotificationInner = (props) => {
  const { message, type, notificationInnerActive, setNotificationInnerActive } = props

  useEffect(() => {
    if (notificationInnerActive) {
      setNotificationInnerActive(true) // сразу показываем

      const timer = setTimeout(async () => {
        setNotificationInnerActive(false)
      }, 3000)
      
      return () => {
        clearTimeout(timer)
      } //отменяем ожидание если элемент notification inner больше не вмонтирован в разметку
    }
  }, [notificationInnerActive])


  return (
    <div
      className={`notification inner 
        ${notificationInnerActive ? "active" : ""}
        ${type}`}
    >
      <p>{message}</p>
    </div>
  )
}

export default NotificationInner
