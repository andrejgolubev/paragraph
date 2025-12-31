import { useEffect, useContext } from "react"
import { Context } from "../../context/Provider"

const NotificationOuter = ({message, type='success'}) => {
  const {homeworkSaved, setHomeworkSaved} = useContext(Context)

  useEffect(() => {
    console.log('homeworkSaved :>> ', homeworkSaved);
    const timer = setTimeout( async () => {
      setHomeworkSaved(false)
    }, 3000)

    return () => clearTimeout(timer) //отменяем ожидание если элемент notification inner больше не вмонтирован в разметку 
  } , [homeworkSaved])
  
  return (
    <div
      className={`notification outer ${
        homeworkSaved ? "active" : ""
      }  ${type}`}
    >
      {message}
    </div>
  )
}

export default NotificationOuter
