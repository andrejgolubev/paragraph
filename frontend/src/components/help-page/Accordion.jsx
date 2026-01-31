import React, { useState } from "react"
import { AccordionItem } from "./AccordionItem"
import { useThemeStore } from "../../store/themeStore"

export const Accordion = ({ faqList }) => {
  const darkTheme = useThemeStore(state => state.darkTheme)
  const [openId, setOpenId] = useState(null)

  
  return (
    <ul className={`accordion ${darkTheme? 'dark' : ''}`}>
      {faqList.map((faqItem, id) => {
        return (
          <AccordionItem
            faqItem={faqItem}
            isOpen={id === openId}
            onClick={() => {
                id === openId ? setOpenId(null) : setOpenId(id)
              }}
            key={id}
          />
        )
      })}
    </ul>
  )
}

export default Accordion
