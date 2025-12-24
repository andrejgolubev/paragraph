import { useCallback } from "react"
import { useEffect } from "react"
import { useState } from "react"
import { render } from "sass"

const Dropdown = (props) => {
  const { name, func, placeholder, readOnly, setTipActive, renderData } = props
  // const [activeSearch, setActiveSearch] = useState(false)

  const [inputText, setInputText] = useState('')

  const handleClick = (event) => {
    setTimeout(() => {
      setTipActive(false)
    }, 300)
  }
  
  
  const onInput = (event) => {
    setInputText(event.target?.value.trim()) 
  }

  // useEffect будет отвечать за ul с группами/датами
  // useEffect( () => )

  return (
    <div className={name} onClick={handleClick} >
      <div className="custom-dropdown">
        <div className={func + "-block"}>
          <div
            className={
              func + "-block__body " + (inputText && "active-search")
            }
          >
            <div className={func + "-block__wrap-input"}>
              <input
                readOnly={readOnly}
                onInput={onInput}
                type="text"
                id={func + "-input"}
                placeholder={placeholder}
                className={func + "-block__input"}
              />
            </div>
            {inputText && 
            (<ul className='search-block__elements'>
              <li><a href="#">render</a></li>
            </ul>)}
            
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dropdown
