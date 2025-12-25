import { createContext, useState } from "react"

export const Context = createContext({})

export const Provider = ({ children }) => {
  const [groupDataValue, setGroupDataValue] = useState("")
  const [dateDataValue, setDateDataValue] = useState("")
  const [homeworkSaved, setHomeworkSaved] = useState(false)

  return (
    <Context.Provider
      value={{
        groupDataValue,
        setGroupDataValue,
        dateDataValue,
        setDateDataValue,
        homeworkSaved, 
        setHomeworkSaved,
        
      }}
    >
      {children}
    </Context.Provider>
  )
}
