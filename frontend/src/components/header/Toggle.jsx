import React from "react"
import { useThemeStore } from "../../store/themeStore"
import toggleBgLight from "../../images/toggles/toggle-bg.svg"
import toggleBgDark from "../../images/toggles/toggle-bg-dark.svg"
import toggleIcon from "../../images/toggles/toggle-icon.svg"
import toggleIconDark from "../../images/toggles/toggle-icon-dark.svg"

export const Toggle = ({isMobile}) => {
  const darkTheme = useThemeStore(state => state.darkTheme)
  const toggleTheme = useThemeStore(state => state.toggleTheme)
  
  return (
    <div 
      className={`toggle ${isMobile? 'mobile' : ''}`} 
      onClick={toggleTheme}
    >
      <img
        id={`toggle-bg${darkTheme ? "-dark" : ""}`}
        src={darkTheme ? toggleBgDark : toggleBgLight}
      />
      <img
        id={`toggle-icon${darkTheme ? "-dark" : ""}`}
        src={darkTheme ? toggleIconDark : toggleIcon}
      />
    </div>
  )
}
