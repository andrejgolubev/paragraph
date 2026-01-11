import { useContext } from "react"
import { Context } from "../../../../context/Provider"

const Button = ({ children, onClick, isActive = false }) => { 
  const {darkTheme} = useContext(Context)

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