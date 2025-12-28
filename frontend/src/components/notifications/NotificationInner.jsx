import { useState, useEffect } from "react"

const NotificationInner = (props) => {
  const { message, type, noTextSubmitError, setNoTextSubmitError } = props


  useEffect(() => {
    const timer = setTimeout( async () => {
      setNoTextSubmitError(false)
    }, 3000)

    return () => clearTimeout(timer) //отменяем ожидание если элемент notification inner больше не вмонтирован в разметку 
  } , [noTextSubmitError])
  
  return (
    <div
      className={`notification inner ${
        noTextSubmitError ? "active" : ""
      }  ${type}`}
    >
      {message}
    </div>
  )
}

export default NotificationInner
