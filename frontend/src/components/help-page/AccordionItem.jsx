import React, { useContext, useRef } from "react"
import dropdownArrow from '../../images/help-page/dropdown-arrow.svg'
import dropdownArrowDark from '../../images/help-page/dropdown-arrow-dark.svg'
import { Context } from "../../context/Provider"

export const AccordionItem = ({ faqItem, onClick, isOpen }) => {
  const {darkTheme} = useContext(Context)

  const itemRef = useRef(null)

  return (
    <li className="accordion__item">
      <button onClick={onClick} className="accordion__header">
        {faqItem.q}
        <img src={darkTheme? dropdownArrowDark : dropdownArrow} className={`accordion__arrow ${isOpen ? 'active' : ''}`}/>
      </button>
      <div
        className='accordion__collapse'
        style={
          isOpen ? { height: itemRef.current.scrollHeight } : { height: "0" }
        }
      >
        <div className={`accordion__body ${darkTheme? 'dark' : ''}`} ref={itemRef}>
          {faqItem.a}
        </div>
      </div>
    </li>
  )
}
