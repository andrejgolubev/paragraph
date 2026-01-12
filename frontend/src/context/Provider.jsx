import { createContext, useEffect} from "react"
import { useAuthStore } from "../store/authStore"
import { useThemeStore } from "../store/themeStore"

export const Context = createContext({})

export const Provider = ({ children }) => {

  const fetchUser = useAuthStore((state) => state.fetchUser)
  const darkTheme = useThemeStore((state) => state.darkTheme)

  useEffect( () => {
    fetchUser()
    document.body.classList.add(darkTheme? 'dark' : 'light')
  }, []) // срабатывает при обновлении страницы 


  return (
    <Context.Provider
    value={{}}
    >
      {children}
    </Context.Provider>
  )
}
