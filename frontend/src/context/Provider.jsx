import { useEffect} from "react"
import { useThemeStore } from "../store/themeStore"
import { Context } from "./AppContext"

export const Provider = ({ children }) => {
  const darkTheme = useThemeStore((state) => state.darkTheme)

  useEffect(() => {
    document.body.classList.toggle("dark", darkTheme)
    document.body.classList.toggle("light", !darkTheme)
  }, [darkTheme])


  return (
    <Context.Provider
    value={{}}
    >
      {children}
    </Context.Provider>
  )
}
