import React, { useRef, useLayoutEffect, useState } from "react"
import dropdownArrow from '../../images/help-page/dropdown-arrow.svg'
import dropdownArrowDark from '../../images/help-page/dropdown-arrow-dark.svg'
import { useThemeStore } from "../../store/themeStore"

export const AccordionItem = ({ faqItem, onClick, isOpen }) => {
  const darkTheme = useThemeStore(state => state.darkTheme)

  const itemRef = useRef(null)
  const [itemHeight, setItemHeight] = useState(0)

  useLayoutEffect(() => {
    const current = itemRef.current
    if (!current) return

    setItemHeight(current.scrollHeight)
  }, [isOpen])
  
  return (
    <li className="accordion__item">
      <button onClick={onClick} className="accordion__header">
        {faqItem.q}
        <img src={darkTheme? dropdownArrowDark : dropdownArrow} className={`accordion__arrow ${isOpen ? 'active' : ''}`}/>
      </button>
      <div
        className='accordion__collapse'
        style={
          isOpen
            ? { height: itemHeight }
            : { height: 0 }
        }
      >
        <div className={`accordion__body ${darkTheme? 'dark' : ''}`} ref={itemRef}>
          {typeof faqItem.a === "string" ? (
            <p>{faqItem.a}</p>
          ) : (
            faqItem.a
          )}
        </div>
      </div>
    </li>
  )
}
