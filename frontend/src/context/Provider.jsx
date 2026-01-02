import { createContext, useEffect, useState } from "react"
import { useCookies } from "react-cookie"

export const Context = createContext({})

export const Provider = ({ children }) => {
  const [homeworkSaved, setHomeworkSaved] = useState(false)
  const [tipActive, setTipActive] = useState(false)
  
  // const cookieGroupDataValue = document.cookie?.split('=')[1] ?? ""

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
        homeworkSaved, 
        setHomeworkSaved,
        tipActive, 
        setTipActive,
        setGroupDataValueCookies,
      }}
    >
      {children}
    </Context.Provider>
  )
}
