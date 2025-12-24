import { createContext, useState } from "react"

export const Context = createContext({})

export const Provider = ({ children }) => {
  const [groupDataValue, setGroupDataValue] = useState("")
  const [dateDataValue, setDateDataValue] = useState("")

  return (
    <Context.Provider
      value={{
        groupDataValue,
        setGroupDataValue,
        dateDataValue,
        setDateDataValue,
      }}
    >
      {children}
    </Context.Provider>
  )
}
