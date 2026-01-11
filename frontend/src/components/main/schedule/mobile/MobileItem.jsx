import paperclip from "../../../../images/homework/paperclip.svg"
import paperclipDark from "../../../../images/homework/paperclip-dark.svg"

import { useContext } from "react"
import { Context } from "../../../../context/Provider"


const MobileItem = ({ time, lessonId, onClick, texts = [], types = [] }) => {
  const { darkTheme } = useContext(Context)

  if (!texts.length && !types.length) return null

  const normalized = texts.map((text, index) => ({
    text: text?.trim(),
    typeColor: types?.[index] ? types.map(type => (
      type === 'Лек.' ? 'lec' : type === 'Упр.' ? 'upr' : type === 'Лаб.' ? 'lab' : type
    ))?.[index].trim() : "",
    type: types?.[index] ? types[index] : "",
    key: `${text}-${index}`,
  }))


  
  return (
    <div data-index={lessonId} className="mobile-schedule__content__item">
      <div className="mobile-schedule__content__item__time" onClick={onClick}>
        <p>{time}</p>
        <img src={darkTheme ? paperclipDark : paperclip} alt="paperclip" />
      </div>
      <div className="mobile-schedule__content__item__text">
        {normalized.map(({ text, type, key, typeColor }, index) =>
          text ? (
            <p key={key}>
              {type && <span className={`mobile-schedule__content__item__text__type`} id={typeColor}>{type}</span>}
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
