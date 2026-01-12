import telegramIcon from "../images/news/telegram-icon.svg"
import telegramIconDark from "../images/news/telegram-icon-dark.svg"
import { useContext } from "react"
import { Context } from "../context/Provider"




const News = () => {

  const {darkTheme} = useContext(Context)
  const url = "https://www.youtube.com/watch?v=IfrBUr9aU5U"

  return (
    <div className={`news-container ${darkTheme ? "dark" : ""}`}>
      <a href={url} target="_blank"><img src={darkTheme ? telegramIconDark : telegramIcon} alt="telegram" /></a>
      <p>Подписывайтесь на 
        <a className={`news-container__link ${darkTheme ? "dark" : ""}`} href={url} target="_blank"> "параграф"
          
        </a> в Telegram и будьте в курсе актуальных событий и обновлений.
      </p>
    </div>
  )
}

export default News