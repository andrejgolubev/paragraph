import React, { useContext, useState } from "react"
import { AccordionItem } from "./AccordionItem"
import { Context } from "../../context/Provider"

export const Accordion = ({ faqList }) => {
  const {darkTheme} = useContext(Context)

  const [openId, setOpenId] = useState(null)

  return (
    <ul className={`accordion ${darkTheme? 'dark' : ''}`}>
      {faqList.map((faqItem, id) => {
        return (
          <AccordionItem
            faqItem={faqItem}
            isOpen={id === openId}
            onClick={() => id === openId ? setOpenId(null) : setOpenId(id)}
            
            key={id}
          />
        )
      })}
    </ul>
  )
}

export default Accordion
