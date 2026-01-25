import { useState, useEffect, useMemo } from "react"
import API, { showNotificationOuter } from "../../api/API"
import { useRef } from "react"
import { useClickOutside } from "../../hooks/useClickOutside"
import { latinToCyrillic } from "../../utils/converters"
import { useDebounce } from "../../hooks/useDebouce"
import { useDropdownStore } from "../../store/dropdownStore"
import { useThemeStore } from "../../store/themeStore"

const Dropdown = ({ name, func, placeholder, readOnly}) => {
  const darkTheme = useThemeStore(state => state.darkTheme)
  
  const [inputText, setInputText] = useState("")
  const [data, setData] = useState([])
  // const [filteredData, setFilteredData] = useState([])
  const [elemKey, setElemKey] = useState("")
  const [activeSearch, setActiveSearch] = useState(false)

  const { groupDataValue, setGroupDataValue, dateDataValue, setDateDataValue } =
    useDropdownStore()

  const dropdownRef = useRef(null)
  const inputRef = useRef("")
  

  // группы и даты не будут сохраняться при перезаходах на "/" без этого эффекта 
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
  }, [groupDataValue, dateDataValue])


  useClickOutside([dropdownRef], () => {
    setActiveSearch(false)
  })


  const debouncedInputText = useDebounce(inputText, 100)

  // фильтрует только для Dropdown с func === 'search'
  const filteredData = useMemo(() => {
    if (!debouncedInputText || func === 'select') return data
    const cleanText = latinToCyrillic(debouncedInputText).trim().toLowerCase()
    return (
      data?.filter((elem) => {
        const element = elem[elemKey]
        return element && element.toLowerCase().trim().includes(cleanText)
      }) ?? []
    )
  }, [data, elemKey, debouncedInputText])


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
      showNotificationOuter(error.message, 'error')
      setActiveSearch(false)
    }
  }


  const handleClick = () => {
    if (name === "group") loadGroups()
    else if (name === "week") loadDates()
    setActiveSearch((prev) => !prev)
  }

  const loadGroups = async () => {
    const responseData = await API.loadGroups()

    setData(responseData)
    setElemKey("group_number")
  }
  
  const loadDates = async () => {
    const responseData = await API.loadDates()

    setData(responseData)
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
