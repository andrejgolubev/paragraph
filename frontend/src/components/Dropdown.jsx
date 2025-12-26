import { useState, useEffect, useContext } from "react"
import homeworkAPI from "../api/homeworkAPI"
import { Context } from "../context/Provider"
import { useRef } from "react"
import { useClickOutside } from "../hooks/useClickOutside"

const Dropdown = (props) => {
  const { name, func, placeholder, readOnly} = props

  const [inputText, setInputText] = useState("")
  const [data, setData] = useState([])
  const [filteredData, setFilteredData] = useState([])
  const [elemKey, setElemKey] = useState("")
  const [activeSearch, setActiveSearch] = useState(false)
  const [error, setError] = useState(false)


  const dropdownRef = useRef(null)
  const inputRef = useRef("")

  useClickOutside([dropdownRef], () => {
    setActiveSearch(false)
  })

  const { groupDataValue, setGroupDataValue, dateDataValue, setDateDataValue } =
    useContext(Context)

  // будет только для "group" ну и для других, где пользователь сам вводит текст
  useEffect(() => {
    setFilteredData(
      data.filter((elem) => {
        const element = elem[elemKey]

        return (
          element &&
          element.toLowerCase().trim().includes(inputText.trim().toLowerCase())
        )
      })
    )
  }, [inputText])

  const handleEnterKey = (event, inputText) => {
    if (event.key === 'Enter') {
      if (name === "group") {
        console.log('inputText :>> ', inputText);
        homeworkAPI.convertToDataValue({groupNumber: inputText})
        .then(resp => resp['group_data_value']).then(responseValue => {
          if (responseValue) {
            setGroupDataValue(responseValue) 
          } else {
            setGroupDataValue('')
            setActiveSearch(false)
            // ТУТ ЧТО ТО ТИПА setError({true, type: 'wrong-group'})

          }
        })
        

      }
    }

  }

  const handleClick = () => {
    if (name === "group") {
      loadGroups()
    } else if (name === "week") {
      loadDates()
      setActiveSearch(true)
    }
    // можно ещё сюда какие угодно добавлять нэймы функция универсальная (почти :) )

  }

  const loadGroups = async () => {
    const responseData = await homeworkAPI.loadGroups()
    setData(responseData)
    // просто setData, т.к. по группам осуществляется ПОИСК и они будут фильтроваться по мере ввода текста, т.е. data -> filteredData
    setElemKey("group_number")
  }

  const loadDates = async () => {
    const responseData = await homeworkAPI.loadDates()
    setFilteredData(responseData)
    // сразу setFilteredData т.к. фильтрация не требуется, выбор даты осуществляткся руками
    setElemKey("date")
  }

  const onInput = (event) => {
    setInputText(event.target?.value.trim())
    setActiveSearch(true)
  }

  const handleSelect = (elem) => {
    inputRef.current.value = elem[elemKey]
    setActiveSearch(false)
    if (name === "group") {
      setGroupDataValue(elem["data_value"])
    } else if (name === "week") {
      setDateDataValue(elem["data_value"])
    }
  }

  

  return (
    <div className={name} onClick={handleClick} ref={dropdownRef}>
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
                onKeyDown={(event) => handleEnterKey(event, inputText)}
              />
            </div>
            {activeSearch && (
              <ul className={func + "-block__elements"}>
                {filteredData.map((elem) => (
                  <li
                    key={elem.id}
                    onClick={(e) => {
                      e.stopPropagation()
                      handleSelect(elem)
                    }}
                  >
                    <a href="#">{elem[elemKey]}</a>
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
