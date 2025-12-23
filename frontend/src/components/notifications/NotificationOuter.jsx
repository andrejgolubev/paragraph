import { useState } from "react"

const NotificationOuter = (props) => {
  const { message, type } = props

  const [notificationShown, setNotificationShown] = useState(false)


  useEffect(() => {
    setNotificationShown(true)
    const timer = setTimeout(() => {
      setNotificationShown(false)
    }, 3000)

    return () => clearTimeout(timer) //отменяем ожидание если элемент notification outer больше не вмонтирован в разметку 
  } , [])
  
  return (
    <div
      className={`notification outer ${
        notificationShown ? "active" : ""
      }  ${type}`}
    >
      {message}
    </div>
  )
}

export default NotificationOuter