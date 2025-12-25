import questionMark from '../images/question-mark.svg'
import exitIcon from '../images/exit-icon.svg'
import { useClickOutside } from '../hooks/useClickOutside'
import { useRef } from 'react'

export const ProfileDropdown = (props) => {
  const {setDisplayProfile} = props

  const dropdownRef = useRef('')

  useClickOutside(dropdownRef, () => {
    setDisplayProfile(false)
  })

  if (props) {
    const { username, role } = props

    return (
      <div className="profile-dropdown" ref={dropdownRef} >
        <div className="profile-dropdown__inner">
          <p>Андрей Голубев</p>
          <p className="role small">Администратор</p>
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
              <img className='options-list__elem__img' src={questionMark} alt="question mark" />
              <a href="#">
                <p>Помощь</p>
              </a>
            </div>
            <div className="options-list__elem">
              <img className='options-list__elem__img' src={exitIcon} alt="exit icon" />
              <a href="#">
                <p>Выход</p>
              </a>
            </div>
          </div>


        </div>
      </div>
    )
  } else {
  }
}
