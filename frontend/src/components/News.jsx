import telegramIcon from "../images/news/telegram-icon.svg"
import telegramIconDark from "../images/news/telegram-icon-dark.svg"
import { useThemeStore } from "../store/themeStore"



const News = () => {

  const darkTheme = useThemeStore(state => state.darkTheme)
  const url = "https://t.me/paragraphschedule"

  return (
    <div className={`news-container ${darkTheme ? "dark" : ""}`}>
      <a href={url} target="_blank"><img src={darkTheme ? telegramIconDark : telegramIcon} alt="telegram" /></a>
      <p>Подписывайтесь на 
        <a className={`news-container__link ${darkTheme ? "dark" : ""}`} href={url} target="_blank"> "параграф"
          
        </a> в Telegram! Любая активность мотивирует меня продолжать разработку.
      </p>
    </div>
  )
}

export default News