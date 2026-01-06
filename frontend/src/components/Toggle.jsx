import React, { useContext } from "react"
import { Context } from "../context/Provider"

import toggleBgLight from "../images/toggles/toggle-bg.svg"
import toggleBgDark from "../images/toggles/toggle-bg-dark.svg"
import toggleIcon from "../images/toggles/toggle-icon.svg"
import toggleIconDark from "../images/toggles/toggle-icon-dark.svg"
import { useWindowSize } from "../hooks/useWindowSize"

export const Toggle = ({isMobile}) => {
  const {darkTheme, setDarkTheme} = useContext(Context)
  return (
    <div 
      className={`toggle ${isMobile? 'mobile' : ''}`} 
      onClick={() => setDarkTheme((prev) => !prev)}
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
