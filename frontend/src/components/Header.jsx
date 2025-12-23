import "../sass/main.scss" // все стили
import logo from "../images/logoAndText.svg"
import toggleBg from "../images/toggle-bg.svg"
import toggleSun from "../images/toggle-sun.svg"
import profileIcon from "../images/ProfileIcon.svg"

const Header = () => {
  return (
    <header className="header">
      <nav className="nav">
        <ul className="nav_list">
          <li className="nav_item">
            <a href="/">
              <img className="nav_logo" src={logo} alt="Logo" />
            </a>
          </li>
          <li>
            <div className="links">
              <li className="nav_item">
                <a href="#">журнал</a>
              </li>
              <li className="nav_item">
                <a href="#">новости</a>
              </li>
              <li className="nav_item">
                <a href="#">о проекте</a>
              </li>
              <div className="toggle">
                <img id="toggle-bg" src={toggleBg} alt="Toggle background" />
                <img id="toggle-sun" src={toggleSun} alt="Toggle sun" />
              </div>
              <img
                src={profileIcon}
                alt="Profile"
                className="profile-icon nav_item"
              />
            </div>
          </li>
        </ul>
      </nav>
    </header>
  )
}

export default Header
