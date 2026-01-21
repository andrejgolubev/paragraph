import { useEffect } from "react"
import { useUiStore } from "../../store/uiStore"


const NotificationOuter = ({type}) => {
  const {
    notificationOuterActive,
    setNotificationOuterActive,
    notificationOuterMessage,
    setNotificationOuterMessage,
    notificationOuterType,
  } = useUiStore()
  
  console.log('NotificationOuter:')
  console.log('notificationOuterActive :>> ', notificationOuterActive);
  console.log('notificationOuterMessage :>> ', notificationOuterMessage);
  console.log('notificationOuterType :>> ', notificationOuterType )
  
  useEffect(() => {
    const timer = setTimeout( async () => {
      setNotificationOuterActive(false)
    }, 3000)

    return () => clearTimeout(timer) //отменяем ожидание если элемент notification inner больше не вмонтирован в разметку 
  } , [notificationOuterActive])


  useEffect( () => {
    return () => setNotificationOuterActive(false) // если компонент размонтирован, скрываем его
  }, [])
  const visualType = type || notificationOuterType 

  return (
    <div
      className={`notification outer ${
        notificationOuterActive ? "active" : ""
      }  ${visualType}`}
    >
      {notificationOuterMessage}
    </div>
  )


}

export default NotificationOuter
