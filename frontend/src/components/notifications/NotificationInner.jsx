import { useState, useEffect } from "react"

const NotificationInner = (props) => {
  const { message, type, notificationInnerActive, setNotificationInnerActive } = props
  const [isActive, setIsActive] = useState(false)

  
  useEffect(() => {
    if (notificationInnerActive) {
      setIsActive(true) // сразу показываем

      const timer = setTimeout(async () => {
        setIsActive(false)
      }, 3000)
      
      return () => {
        clearTimeout(timer)
      } //отменяем ожидание если элемент notification inner больше не вмонтирован в разметку
    }

  }, [
    notificationInnerActive
  ])

  return (
    <div
      className={`notification inner 
        ${isActive ? "active" : ""}
        ${type}`}
    >
      <p>{message}</p>
    </div>
  )
}

export default NotificationInner
