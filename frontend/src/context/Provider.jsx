import { useEffect} from "react"
import { useAuthStore } from "../store/authStore"
import { useThemeStore } from "../store/themeStore"
import { Context } from "./AppContext"

export const Provider = ({ children }) => {

  const fetchUser = useAuthStore((state) => state.fetchUser)
  const darkTheme = useThemeStore((state) => state.darkTheme)

  useEffect( () => {
    fetchUser()
  }, []) // срабатывает при обновлении страницы 
  
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
