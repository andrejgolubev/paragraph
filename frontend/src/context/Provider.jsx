import { createContext, useEffect, useState } from "react"
import { useCookies } from "react-cookie"

export const Context = createContext({})

export const Provider = ({ children }) => {
  // уведомления по типу "дз сохранено" , "успешный вход в аккаунт"
  const [notificationOuterMessage, setNotificationOuterMessage] = useState('')
  const [notificationOuterActive, setNotificationOuterActive] = useState(false)

  const [tipActive, setTipActive] = useState(false) //подсказка при первом заходе на сайт
  
  // клиентские куки
  const [groupDataValueCookies, setGroupDataValueCookies, removeGroupDataValueCookies] = useCookies(['group_data_value'])
  const groupDataValueCookie = groupDataValueCookies.groupDataValue
  const [groupDataValue, setGroupDataValue] = useState(groupDataValueCookie)


  const [dateDataValue, setDateDataValue] = useState("")

  
  return (
    <Context.Provider
      value={{
        groupDataValue,
        setGroupDataValue,
        dateDataValue,
        setDateDataValue,
        notificationOuterActive, 
        setNotificationOuterActive,
        tipActive, 
        setTipActive,
        setGroupDataValueCookies,
        notificationOuterMessage, 
        setNotificationOuterMessage,
      }}
    >
      {children}
    </Context.Provider>
  )
}
