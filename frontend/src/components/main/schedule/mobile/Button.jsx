
import { useThemeStore } from "../../../../store/themeStore"

const Button = ({ children, onClick, isActive = false }) => { 
  const darkTheme = useThemeStore(state => state.darkTheme)

  return (
    <button 
      className={
        `mobile-schedule__header__button 
        ${isActive? 'active': ''} ${darkTheme? 'dark': ''}`
      } 
      onClick={onClick}>
      {children}
    </button>
  )
}

export default Button