import { useEffect } from "react"
import { useUiStore } from "../../store/uiStore"


const NotificationOuter = ({type='success'}) => {
  const {notificationOuterActive, setNotificationOuterActive, notificationOuterMessage, setNotificationOuterMessage} = useUiStore()
  

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
      {notificationOuterMessage}
    </div>
  )


}

export default NotificationOuter
