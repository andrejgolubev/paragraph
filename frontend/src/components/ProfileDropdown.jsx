import questionMark from "../images/question-mark.svg"
import exitIcon from "../images/exit-icon.svg"
import closeIcon from "../images/close-icon.svg"
import loginIcon from '../images/login-icon.svg'
import registerIcon from '../images/register-icon.svg'


export const ProfileDropdown = (props) => {
  const { setDisplayProfile, dropdownRef, username, role } = props

  if (username && role) {
    return (
      <div className="profile-dropdown" ref={dropdownRef}>
        <img
          className="profile-dropdown__close"
          src={closeIcon}
          onClick={() => setDisplayProfile(false)}
        ></img>
        <div className="profile-dropdown__inner">
          <p>{username}</p>
          <p className="role small">{role}</p>
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
            <div className="options-list__elem">
              <img
                className="options-list__elem__img"
                src={questionMark}
              />
              <a href="#">
                <p>Помощь</p>
              </a>
            </div>
            <div className="options-list__elem">
              <img
                className="options-list__elem__img"
                src={exitIcon}
              />
              <a href="#">
                <p>Выход</p>
              </a>
            </div>
          </div>
        </div>
      </div>
    )
  } else {
    return (
      <div className="profile-dropdown" ref={dropdownRef}>
        <img
          className="profile-dropdown__close"
          src={closeIcon}
          onClick={() => setDisplayProfile(false)}
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
          <div className="options-list" >
            <div className="options-list__elem" style={{gap: '6px'}}>
              <img
                className="options-list__elem__img"
                src={loginIcon}
              />
              <a href="#">
                <p>Вход</p>
              </a>
            </div>
            <div className="options-list__elem" style={{gap: '3px'}}>
              <img
                className="options-list__elem__img"
                src={registerIcon}
              />
              <a href="#" style={{position: 'relative', top: '1px'}}>
                <p>Регистрация</p>
              </a>
            </div>
            <div className="options-list__elem">
              <img
                className="options-list__elem__img"
                src={questionMark}
              />
              <a href="#">
                <p>Помощь</p>
              </a>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
