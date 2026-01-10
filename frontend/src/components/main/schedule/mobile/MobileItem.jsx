import paperclip from "../../../../images/homework/paperclip.svg"
import paperclipDark from "../../../../images/homework/paperclip-dark.svg"

import { useContext } from "react"
import { Context } from "../../../../context/Provider"


const MobileItem = ({ time, text }) => {
  const {darkTheme} = useContext(Context)
  const textArray = text.split(", ")

  return (
    <div className="mobile-schedule__content__item">
      <div className="mobile-schedule__content__item__time">
        <p>{time}</p>
        <img src={darkTheme? paperclipDark : paperclip} alt="paperclip" />
      </div>
      <div className="mobile-schedule__content__item__text">
        {textArray.map((item, index) => (
          <p key={index}>{item}{index < textArray.length - 1 ? "," : ""}</p>
        ))}
      </div>
    </div>
  )
}

export default MobileItem
