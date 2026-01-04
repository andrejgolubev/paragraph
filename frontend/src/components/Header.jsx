
import paragraphLogo from "../images/logos/paragraph-logo.svg"
import paragraphLogoDark from "../images/logos/paragraph-logo-dark.svg"
import toggleBgLight from "../images/toggles/toggle-bg.svg"
import toggleBgDark from "../images/toggles/toggle-bg-dark.svg"
import toggleIcon from "../images/toggles/toggle-icon.svg"
import toggleMoon from "../images/toggles/toggle-icon-dark.svg"
import profileIcon from "../images/profile-dropdown/profile-icon.svg"
import profileIconDark from "../images/profile-dropdown/profile-icon-dark.svg"
import { ProfileDropdown } from "./ProfileDropdown"
import { useState, useRef, useContext } from "react"
import { useClickOutside } from "../hooks/useClickOutside"
import { Link, useLocation } from "react-router-dom"
import { Context } from "../context/Provider"

const Header = () => {
  const { darkTheme, setDarkTheme } = useContext(Context)

 
  const [displayProfile, setDisplayProfile] = useState(false)
  const dropdownRef = useRef(null)
  const profileRef = useRef(null)
  const location = useLocation()

  const {username, userRole} = useContext(Context)
  useClickOutside([dropdownRef, profileRef], () => {
    setDisplayProfile(false)
  })

  return (
    <header className={`header ${darkTheme? 'dark' : ''}`}>
      <nav className="nav">
        <ul className="nav_list">
          <Link to="/">
            <li className="nav_item">
              <p>
                <img 
                className="nav_logo" 
                src={darkTheme? paragraphLogoDark : paragraphLogo} 
                alt="Logo" 
                />
              </p>
            </li>
          </Link>
          <li>
            <div className="links">
              <Link to="/">
                <div
                  className={`nav_item ${
                    location.pathname === "/" ? "bold" : ""
                  }`}
                >
                  <p>дневник</p>
                </div>
              </Link>
              <div
                className={`nav_item ${
                  location.pathname === "/news" ? "bold" : ""
                }`}
              >
                <p>новости</p>
              </div>
              <Link to="/help">
                <div
                  className={`nav_item ${
                    location.pathname === "/help" ? "bold" : ""
                  }`}
                >
                  <p>о проекте</p>
                </div>
              </Link>

              <div
                className="toggle"
                onClick={() => setDarkTheme((prev) => !prev)}
              >
                <img
                  id={`toggle-bg${darkTheme ? "-dark" : ''}`}
                  src={darkTheme ? toggleBgDark : toggleBgLight}
                />
                <img 
                id={`toggle-icon${darkTheme ? "-dark" : ''}`} 
                src={darkTheme ? toggleMoon : toggleIcon} />
              </div>
              <img
                ref={profileRef}
                src={profileIcon}
                onClick={(e) => {
                  e.preventDefault()
                  setDisplayProfile((prev) => !prev)
                }}
                alt="Profile"
                className="profile-icon nav_item"
              />
              {displayProfile && (
                <ProfileDropdown
                  username={username}
                  role={userRole}
                  dropdownRef={dropdownRef}
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
