
import logo from "../images/logoAndText2.svg"
import toggleBg from "../images/toggle-bg.svg"
import toggleSun from "../images/toggle-sun.svg"
import profileIcon from "../images/ProfileIcon.svg"
import { ProfileDropdown } from "./ProfileDropdown"
import { useState, useRef, useContext } from "react"
import { useClickOutside } from "../hooks/useClickOutside"
import { Link, useLocation } from "react-router-dom"
import { Context } from "../context/Provider"

const Header = () => {

  const [displayProfile, setDisplayProfile] = useState(false)
  const dropdownRef = useRef(null)
  const profileRef = useRef(null)
  const location = useLocation()

  const {username, userRole} = useContext(Context)
  useClickOutside([dropdownRef, profileRef], () => {
    setDisplayProfile(false)
  })

  return (
    <header className="header">
      <nav className="nav">
        <ul className="nav_list">
          <Link to='/'>
            <li className="nav_item">
              <p>
                <img className="nav_logo" src={logo} alt="Logo" />
              </p>
            </li>
          </Link>
          <li>
            <div className="links">
              <Link to='/'>
                <div className={`nav_item ${location.pathname === '/' ? 'bold' : ''}`} >
                  <p>дневник</p>
                </div>
              </Link>
                <div className={`nav_item ${location.pathname === '/news' ? 'bold' : ''}`} >
                  <p>новости</p>
                </div>
              <Link to='/help'>
                <div className={`nav_item ${location.pathname === '/help' ? 'bold' : ''}`}>
                  <p>о проекте</p>
                </div>
              </Link>
              <div className="toggle">
                <img id="toggle-bg" src={toggleBg} alt="Toggle background" />
                <img id="toggle-sun" src={toggleSun} alt="Toggle sun" />
              </div>
              <img
                ref={profileRef}
                src={profileIcon}
                onClick={ (e) => {
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
