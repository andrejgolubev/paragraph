import React, { useState } from "react"
import { AccordionItem } from "./AccordionItem"

export const Accordion = ({ faqList }) => {
  const [openId, setOpenId] = useState(null)

 

  return (
    <ul className="accordion">
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
