import paperclip from "../../../../images/homework/paperclip.svg"
import paperclipDark from "../../../../images/homework/paperclip-dark.svg"
import { useThemeStore } from "../../../../store/themeStore"


const MobileItem = ({ time, onClick, hasHomework, texts = [], types = [] }) => {
  const darkTheme = useThemeStore(state => state.darkTheme)

  if (!texts.length && !types.length) return null

  const normalized = texts.map((text, index) => ({
    text: text?.trim(),
    typeColor: types?.[index] ? types.map(type => (
      type === 'Лек.' ? 'lec' 
      : type === 'Упр.' ? 'upr' 
      : type === 'Лаб.' ? 'lab' 
      : type === 'Экзамен' ? 'exam' 
      : type === 'Зач.' ? 'cred' 
      : type === 'Конс.' ? 'consult' 
      : type
    ))?.[index].trim() : "",
    type: types?.[index] ? types[index] : "",
    key: `${text}-${index}`,
  }))


  
  return (
    <div className={`mobile-schedule__content__item ${hasHomework ? ' active' : ''} `}>
      <div className="mobile-schedule__content__item__time" onClick={onClick}>
        <p style={{fontWeight: hasHomework? 700 : 500}}>{time}</p>
        <img 
          src={darkTheme ? paperclipDark : paperclip} 
          alt="paperclip" 
          style={{opacity: hasHomework ? 1 : 0.6}}
        />
      </div>
      <div className="mobile-schedule__content__item__text">
        {normalized.map(({ text, type, key, typeColor }, index) =>
          text ? (
            <p 
              key={key}
              
            >
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
