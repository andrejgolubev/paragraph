import "../sass/main.scss" // все стили
import logo from "../images/logoAndText.svg"
import toggleBg from "../images/toggle-bg.svg"
import toggleSun from "../images/toggle-sun.svg"
import profileIcon from "../images/ProfileIcon.svg"
import { ProfileDropdown } from "./ProfileDropdown"
import { useState } from "react"

const Header = () => {

  const [displayProfile, setDisplayProfile] = useState(false)

  return (
    <header className="header">
      <nav className="nav">
        <ul className="nav_list">
          <li className="nav_item">
            <a href="#">
              <img className="nav_logo" src={logo} alt="Logo" />
            </a>
          </li>
          <li>
            <div className="links">
              <div className="nav_item">
                <a href="#">журнал</a>
              </div>
              <div className="nav_item">
                <a href="#">новости</a>
              </div>
              <div className="nav_item">
                <a href="#">о проекте</a>
              </div>
              <div className="toggle">
                <img id="toggle-bg" src={toggleBg} alt="Toggle background" />
                <img id="toggle-sun" src={toggleSun} alt="Toggle sun" />
              </div>
              <img
                src={profileIcon}
                onClick={ () => setDisplayProfile((prev) => !prev)}
                alt="Profile"
                className="profile-icon nav_item"
              />
              {displayProfile && (
                <ProfileDropdown
                setDisplayProfile={setDisplayProfile}
                 />
              )}
            </div>
          </li>
        </ul>
      </nav>
    </header>
  )
}

export default Header
