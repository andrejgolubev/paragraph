import { useEffect, useContext } from "react"
import { Context } from "../../context/Provider"

const NotificationOuter = ({message, type='success'}) => {
  const {notificationOuterActive, setNotificationOuterActive} = useContext(Context)

  useEffect(() => {
    const timer = setTimeout( async () => {
      setNotificationOuterActive(false)
    }, 3000)

    return () => clearTimeout(timer) //отменяем ожидание если элемент notification inner больше не вмонтирован в разметку 
  } , [notificationOuterActive])


  useEffect( () => {
    return () => setNotificationOuterActive(false) // если компонент размонтирован, скрываем его
  }, [])
  return (
    <div
      className={`notification outer ${
        notificationOuterActive ? "active" : ""
      }  ${type}`}
    >
      {message}
    </div>
  )


}

export default NotificationOuter
