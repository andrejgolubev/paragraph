import questionMark from "../../images/profile/profile-dropdown/question-icon.svg" 
import exitIcon from "../../images/profile/profile-dropdown/exit-icon.svg"
import closeIcon from "../../images/profile/profile-dropdown/close-icon.svg"
import loginIcon from "../../images/profile/profile-dropdown/login-icon.svg"
import registerIcon from "../../images/profile/profile-dropdown/register-icon.svg"
import profileIcon from "../../images/profile/profile-dropdown/profile-icon.svg"


import { Link, useNavigate, useLocation } from "react-router-dom"
import { useContext } from "react"
import homeworkAPI from "../../api/homeworkAPI"
import { Context } from "../../context/Provider"
import { useModeratedGroups } from "../../hooks/useModeratedGroups"

export const ProfileDropdown = (props) => {
  const navigate = useNavigate()
  const location = useLocation()
  const path = location.pathname.split('/').pop()

  
  const {darkTheme} = useContext(Context)

  const { setDisplayProfile, dropdownRef, username, role } = props

  const { displayRole, moderatedGroups } = useModeratedGroups()
  

  const { setNotificationOuterActive, setNotificationOuterMessage } =
    useContext(Context) 

  const disappearOnClick = () => setDisplayProfile(false)

  
  const handleLogout = () => {
    if (path === 'profile') {
      navigate('/sign-in')
    }
    homeworkAPI.logout().then( resp => {
      setNotificationOuterActive(true)// чтобы вызвалась проверка access_token (т.к. в Provider такая dependency)
      setNotificationOuterMessage(resp.detail)
    })
    setDisplayProfile(false)
  }


  if (username && role) {
    return (
      <div className={`profile-dropdown ${darkTheme? 'dark' : ''}`} ref={dropdownRef}>
        <img
          className="profile-dropdown__close"
          src={closeIcon}
        ></img>
        <div className="profile-dropdown__inner">
          <p>{username}</p>
          <p className="role small">
            {displayRole}
          </p>
          <p className="small">
            {`${moderatedGroups}`}
          </p>
          <div className="stroke">
            <svg
              width="270"
              height="1"
              viewBox="0 0 270 1"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M0 0.5H258" stroke="#323342" />
            </svg>
          </div>
          <div className="options-list">
            <Link to="/profile">
              <div className="options-list__elem" >
                <img className="options-list__elem__img" src={profileIcon} onClick={disappearOnClick} />
                  <p>Профиль</p>
              </div>
            </Link>
            <Link to="/help">
              <div className="options-list__elem" >
                <img className="options-list__elem__img" src={questionMark} onClick={disappearOnClick} />
                  <p>Помощь</p>
              </div>
            </Link>
            <div className="options-list__elem" onClick={handleLogout}>
              <img className="options-list__elem__img" src={exitIcon} />
                <p>Выход</p>
            </div>
          </div>
        </div>
      </div>
    )
  } else {
    return (
      <div className={`profile-dropdown ${darkTheme? 'dark' : ''}`} ref={dropdownRef}>
        <img
          className="profile-dropdown__close"
          src={closeIcon}
          onClick={disappearOnClick}
        ></img>
        <div className="profile-dropdown__inner">
          <p className="role small">*Вы не вошли в аккаунт*</p>
          <div className="stroke">
            <svg
              width="270"
              height="1"
              viewBox="0 0 270 1"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M0 0.5H258" stroke="#323342" />
            </svg>
          </div>
          <div className="options-list">
            <Link to="/sign-in">
              <div className="options-list__elem" style={{ gap: "6px" }} onClick={disappearOnClick}>
                <img className="options-list__elem__img" src={loginIcon} />
                <p>Вход</p>
              </div>
            </Link>
            <Link to="/sign-up">
              <div className="options-list__elem" style={{ gap: "3px" }} onClick={disappearOnClick}>
                <img className="options-list__elem__img" src={registerIcon} />
                <p style={{ position: "relative", top: "1px" }}>Регистрация</p>
              </div>
            </Link>
            <Link to="/help">
              <div className="options-list__elem">
                <img className="options-list__elem__img" src={questionMark} onClick={disappearOnClick}/>
                <p>Помощь</p>
              </div>
            </Link>
          </div>
        </div>
      </div>
    )
  }
}
