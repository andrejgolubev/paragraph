import { Link } from "react-router-dom"


export const PageNotFound = () => {
  return (
    <div className="not-found">
      <p>Страница не найдена :(</p>
      <p><Link to='/'>Вернёмся к дневнику?</Link></p>
    </div>
  )
}
