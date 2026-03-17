import ScheduleContainer from "./schedule/ScheduleContainer"
import Dropdown from "./Dropdown"
import Tip from "./Tip"
import { useEffect, useState } from "react"
import { useWindowSize } from "../../hooks/useWindowSize"
import { useDropdownStore } from "../../store/dropdownStore"
import { useThemeStore } from "../../store/themeStore"
import { useUiStore } from "../../store/uiStore"
import notesToggle from "../../images/toggles/notes.svg"
import notesToggleDark from "../../images/toggles/notes-dark.svg"
import notesToggleActive from "../../images/toggles/notes_active.svg"
import notesToggleDarkActive from "../../images/toggles/notes-dark_active.svg"
import { showNotificationOuter } from "../../api/API"

const MainContent = () => {
  const { groupDataValue, dateDataValue } = useDropdownStore()
  const { darkTheme } = useThemeStore()
  const { tipActive, setTipActive } = useUiStore()
  const [notesClicked, setNotesClicked] = useState(false)
  const { width } = useWindowSize()
  const isMobile = width < 1001

  useEffect(() => {
    if (groupDataValue) {
      setTipActive(false)
    } else {
      setTipActive(true)
    }
  }, [groupDataValue, setTipActive])


  const handleNotesIconClick = () => {
    setNotesClicked(!notesClicked)
    showNotificationOuter(`режим заметок ${!notesClicked? 'включен' : 'выключен'}`, 'success')
  }

  return (
    <div className="main-content">
      <div
        className={`schedule-wrap ${isMobile ? "mobile" : ""} ${darkTheme ? "dark" : ""}`}
      >
        <div className="options">
          <Dropdown
            name="group"
            func="search"
            placeholder="группа"
            readOnly={false}
          />
          <Dropdown
            name="week"
            func="select"
            placeholder="неделя"
            readOnly={true}
          />
          <div className="corpuses">
            <p>C - Центральный корпус⠀⠀⠀⠀B - Бизнес-инкубатор</p>
            <p>L - Лабораторный корпус ⠀⠀⠀F - Первый корпус</p>
          </div>
          <div className="notes-toggle-container">
            <img
              className="notes-toggle"
              title='Режим заметок'
              onClick={handleNotesIconClick}
              src={
                darkTheme
                  ? notesClicked
                    ? notesToggleDarkActive
                    : notesToggleDark
                  : notesClicked
                    ? notesToggleActive
                    : notesToggle
              }
              alt="Заметки"
            />
          </div>
        </div>
        {!groupDataValue && <Tip active={tipActive} />}
        {groupDataValue && (
          <ScheduleContainer
            groupDataValue={groupDataValue}
            dateDataValue={dateDataValue}
          />
        )}
      </div>
    </div>
  )
}

export default MainContent
