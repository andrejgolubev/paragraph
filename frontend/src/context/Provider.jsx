import { createContext, useState } from "react"

export const Context = createContext({})

export const Provider = ({ children }) => {
  const [groupDataValue, setGroupDataValue] = useState("")
  const [dateDataValue, setDateDataValue] = useState("")
  const [homeworkSaved, setHomeworkSaved] = useState(false)
  const [tipActive, setTipActive] = useState(false)

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
        
      }}
    >
      {children}
    </Context.Provider>
  )
}
