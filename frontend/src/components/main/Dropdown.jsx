import { useState, useEffect } from "react"
import API from "../../api/API"
import { useRef } from "react"
import { useClickOutside } from "../../hooks/useClickOutside"
import { latinToCyrillic } from "../../utils/converters"
import { useDebounce } from "../../hooks/useDebouce"
import { useDropdownStore } from "../../store/dropdownStore"
import { useThemeStore } from "../../store/themeStore"

const Dropdown = (props) => {
  const darkTheme = useThemeStore(state => state.darkTheme)

  const { name, func, placeholder, readOnly} = props
  
  const [inputText, setInputText] = useState("")
  const [data, setData] = useState([])
  const [filteredData, setFilteredData] = useState([])
  const [elemKey, setElemKey] = useState("")
  const [activeSearch, setActiveSearch] = useState(false)

  const dropdownRef = useRef(null)
  const inputRef = useRef("")

  useEffect( () => {
    if (func === 'search') {
      API.convertFromDataValue({groupDataValue}).then(resp => {
        inputRef.current.value = resp?.group_number ?? "" 
      })
    }
    if (func === 'select') {
      API.convertFromDataValue({dateDataValue}).then(resp => {
        inputRef.current.value = resp?.date ?? "" 
      })
    }
  }, [])

   


  useClickOutside([dropdownRef], () => {
    setActiveSearch(false)
  })

  const { groupDataValue, setGroupDataValue, dateDataValue, setDateDataValue } =
    useDropdownStore()

  const debouncedInputText = useDebounce(inputText, 100)

  // будет только для "group" ну и для других, где пользователь сам вводит текст
  useEffect(() => {
    setFilteredData(
      data?.filter((elem) => {
        
        const element = elem[elemKey]

        return (
          element && (
            element.toLowerCase().trim()
            .includes(latinToCyrillic(inputText).trim().toLowerCase())
          )
        )
      })
    )
  }, [debouncedInputText])


  const handleEnterKey = async (event, inputText) => {
    if (event.key !== "Enter" || name !== "group") return
    try {
      const resp = await API.convertToDataValue({ groupNumber: inputText })
      const responseValue = resp["group_data_value"]
      if (responseValue) {
        setGroupDataValue(responseValue)
      } else {
        setGroupDataValue("")
        setActiveSearch(false)
      }
    } catch (error) {
      console.error(error)
    }
  }


  const handleClick = () => {
    if (name === "group") {
      loadGroups()
    } else if (name === "week") {
      loadDates()
    }

    setActiveSearch((prev) => !prev)
  }

  const loadGroups = async () => {
    const responseData = await API.loadGroups()
    console.log('responseData from loadGroups :>> ', responseData);
    setData(responseData)
    // просто setData, т.к. по группам осуществляется ПОИСК и они будут фильтроваться по мере ввода текста, т.е. data -> filteredData
    setElemKey("group_number")
  }
  
  const loadDates = async () => {
    const responseData = await API.loadDates()
    console.log('responseData from loadDates :>> ', responseData);
    setData(responseData) 
    setFilteredData(responseData)
    // сразу setFilteredData т.к. фильтрация не требуется, выбор даты осуществляткся руками
    setElemKey("date")
  }

  const onInput = (event) => {
    const trimmedText = event.target?.value.trim() 
    setInputText(trimmedText )
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
    <div 
    className={name} 
    onClick={handleClick} 
    ref={dropdownRef}>
      <div className={`custom-dropdown ${darkTheme? 'dark' : ''}`}>
        <div className={func + "-block"}>
          <div
            className={
              func + "-block__body " + (activeSearch ? "active-search" : '') + (
                darkTheme ? ' dark' : '' 
              )
            }
          >
            <div className={func + `-block__wrap-input ${darkTheme? 'dark' : ''}` }>
              <input
                ref={inputRef}
                readOnly={readOnly}
                onInput={onInput}
                type="text"
                id={func + "-input"}
                placeholder={placeholder}
                className={func + "-block__input"}
                onKeyDown={(event) => handleEnterKey(event, inputText)}
                autoComplete="off"
              />
            </div>
            {activeSearch && (
              <ul className={func + `-block__elements ${darkTheme? 'dark' : ''}`}>
                {(Array.isArray(filteredData) ? filteredData : []).map((elem, id) => (
                  <li
                    key={id}
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
