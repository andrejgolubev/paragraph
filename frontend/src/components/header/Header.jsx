import paragraphLogo from "../../images/logos/paragraph-logo.svg"
import paragraphLogoDark from "../../images/logos/paragraph-logo-dark.svg"

import profileIcon from "../../images/profile/profile-dropdown/profile-button.svg"
import profileIconDark from "../../images/profile/profile-dropdown/profile-button-dark.svg"
import burgerButton from '../../images/mobile/burger-button.svg'
import burgerButtonDark from '../../images/mobile/burger-button-dark.svg'
import { ProfileDropdown } from "../ProfileDropdown"
import { useState, useRef, useContext } from "react"
import { useClickOutside } from "../../hooks/useClickOutside"
import { Link, useLocation } from "react-router-dom"
import { Context } from "../../context/Provider"
import { useWindowSize } from "../../hooks/useWindowSize"
import { Toggle } from "./Toggle"
import { NavItem } from "./NavItem"


const Header = () => {
  const { darkTheme, username, userRole, linksActive, setLinksActive } = useContext(Context)

  const [displayProfile, setDisplayProfile] = useState(false)
  const dropdownRef = useRef(null)
  const profileRef = useRef(null)
  const location = useLocation()
  
  useClickOutside([dropdownRef, profileRef], () => {
    setDisplayProfile(false)
  })

  const {width} = useWindowSize()
  const isMobile = width < 1001
  
  const [isClosing, setIsClosing] = useState(false)

  const openMenu = () => {
    setIsClosing(false)
    setLinksActive(true)
  }
  
  const closeMenu = () => {
    setIsClosing(true)
    setTimeout(() => {
      setLinksActive(false)
      setIsClosing(false)
    }, 300) // та же длительность, что и в SCSS
  }


  const handleBurgerButtonClick = () => {
    if (linksActive) closeMenu() 
    else openMenu()
  }

  return (
    <header className={`header ${darkTheme? 'dark' : ''}`}>
      <nav className="nav">
        <ul className='nav_list'>
          <Link to="/">
            <li className="nav_item">
              <img 
              className={`nav_logo ${linksActive? 'fixed' : ''}`} 
              src={darkTheme? paragraphLogoDark : paragraphLogo} 
              alt="Logo" 
              />
            </li>
          </Link>
          <li className={`nav_links_container`}>
            <div className={`links  ${linksActive? 'active' : ''} ${darkTheme? 'dark' : ''}
            ${isClosing ? 'closing ' : ''}`}>

              <NavItem path={'/'}> дневник </NavItem>
              <NavItem path={'/news'}> новости </NavItem>
              <NavItem path={'/help'}> о проекте </NavItem>
              
              { !isMobile && <Toggle />}
              
              {isMobile 
                ? (
                  username
                    ? <NavItem path={'/profile'}> профиль </NavItem>
                    : (
                      <>
                        <NavItem path={'/sign-in'}> вход </NavItem>
                        <NavItem path={'/sign-up'}> регистрация </NavItem>
                      </>
                    )
                ) : (
                  <img
                    className="profile-button nav_item"
                    ref={profileRef}
                    src={darkTheme? profileIconDark : profileIcon}
                    onClick={(e) => {
                      e.preventDefault()
                      setDisplayProfile((prev) => !prev)
                    }}
                    alt="Profile"
                  />
                )}
            </div>
            {displayProfile && (
              <ProfileDropdown
              username={username}
              role={userRole}
              dropdownRef={dropdownRef}
              setDisplayProfile={setDisplayProfile}
              />
            )}
          </li>
            {isMobile && <Toggle isMobile={isMobile} />}
            <img 
              onClick={handleBurgerButtonClick}
              className={`burger-button ${linksActive? 'fixed' : ''}`}
              src={darkTheme ? burgerButtonDark : burgerButton}
            />
        </ul>
      </nav>
    </header>
  )
}

export default Header
