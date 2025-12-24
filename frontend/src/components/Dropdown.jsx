import { useState, useEffect, useContext } from "react"
import homeworkAPI from "../api/homeworkAPI"
import { Context } from "../context/Provider"
import { useRef } from "react"
import { useInsertionEffect } from "react"

const Dropdown = (props) => {
  const { name, func, placeholder, readOnly, setTipActive } = props

  const [inputText, setInputText] = useState("")
  const [data, setData] = useState([])
  const [filteredData, setFilteredData] = useState([])
  const [elemKey, setElemKey] = useState("")
  const [activeSearch, setActiveSearch] = useState(false)


  const { groupDataValue, setGroupDataValue, dateDataValue, setDateDataValue } =
    useContext(Context)

  const inputRef = useRef('')  

  // будет только для "group" ну и для других, где пользователь сам вводит текст 
  useEffect( () => {
    setFilteredData(
      data.filter((elem) => {
        const element = elem[elemKey]
        return element && element.includes(inputText)
      })
    )
  }, [inputText])


  const handleClick = () => {
    if (name === "group") {
      loadGroups()
      
    }
    else if (name === "week") {
      loadDates()
      setActiveSearch(true)
    }
    // можно ещё сюда какие угодно добавлять нэймы функция универсальная (почти :) )

    setTipActive(false)
  }

  const loadGroups = async () => {
    const responseData = await homeworkAPI.loadGroups()
    setData(responseData)
    setElemKey("group_number")
  }

  const loadDates = async () => {
    const responseData = await homeworkAPI.loadDates()
    setFilteredData(responseData)
    setElemKey("date")
  }

  const onInput = (event) => {
    setInputText(event.target?.value.trim())
    setActiveSearch(true)
  }

  return (
    <div className={name} onClick={handleClick}>
      <div className="custom-dropdown">
        <div className={func + "-block"}>
          <div
            className={
              func + "-block__body " + (activeSearch && "active-search")
            }
          >
            <div className={func + "-block__wrap-input"}>
              <input
                ref={inputRef}
                readOnly={readOnly}
                onInput={onInput}
                type="text"
                id={func + "-input"}
                placeholder={placeholder}
                className={func + "-block__input"}
              />
            </div>
            {activeSearch && (
              <ul className={func + "-block__elements"}>
                {filteredData.map((elem) => (
                  <li key={elem.id}>
                    <a
                      href="#"
                      onClick={() => {
                        inputRef.current.value = elem[elemKey] 
                        if (name === "group") {
                          setGroupDataValue(elem['data_value'])
                        }
                        else if (name === "week") {
                          setDateDataValue(elem['data_value'])
                        }
                        setTimeout(() => {
                          setActiveSearch(false)
                        }, 600)
                      }}
                    >
                      {elem[elemKey]}
                    </a>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dropdown
