import paperclip from "../../../../images/homework/paperclip.svg"
import paperclipDark from "../../../../images/homework/paperclip-dark.svg"

import { useContext } from "react"
import { Context } from "../../../../context/Provider"


const MobileItem = ({ time, lessonId, texts = [], types = [] }) => {
  const { darkTheme } = useContext(Context)

  if (!texts.length && !types.length) return null

  const normalized = texts.map((text, index) => ({
    text: text?.trim(),
    type: types?.[index] ? types[index].trim() : "",
    key: `${text}-${index}`,
  }))
  console.log('lessonId :>> ', lessonId)
  return (
    <div data-index={lessonId} className="mobile-schedule__content__item">
      <div className="mobile-schedule__content__item__time">
        <p>{time}</p>
        <img src={darkTheme ? paperclipDark : paperclip} alt="paperclip" />
      </div>
      <div className="mobile-schedule__content__item__text">
        {normalized.map(({ text, type, key }, index) =>
          text ? (
            <p key={key}>
              {type && <span className="mobile-schedule__content__item__text__type">{type}</span>}
              {type ? " " : ""}
              {text}
              {index < normalized.length - 1 ? "," : ""}
            </p>
          ) : null
        )}
      </div>
    </div>
  )
}

export default MobileItem
