import { useState, useEffect } from "react"

const NotificationInner = (props) => {
  const { message, type } = props

  const [notificationShown, setNotificationShown] = useState(false)


  useEffect(() => {
    setNotificationShown(true)
    const timer = setTimeout(() => {
      setNotificationShown(false)
    }, 3000)

    return () => clearTimeout(timer) //отменяем ожидание если элемент notification inner больше не вмонтирован в разметку 
  } , [])
  
  return (
    <div
      className={`notification inner ${
        notificationShown ? "active" : ""
      }  ${type}`}
    >
      {message}
    </div>
  )
}

export default NotificationInner
