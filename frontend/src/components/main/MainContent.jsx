import ScheduleContainer from "./schedule/ScheduleContainer" 
import Dropdown from "./Dropdown"
import Tip from "./Tip"
import { useEffect } from "react"
import NotificationOuter from "../notifications/NotificationOuter"
import { useWindowSize } from "../../hooks/useWindowSize"
import { useDropdownStore } from "../../store/dropdownStore"
import { useThemeStore } from "../../store/themeStore"
import { useUiStore } from "../../store/uiStore"
import { useAuthStore } from "../../store/authStore"

const MainContent = () => {
  const { groupDataValue, dateDataValue, } = useDropdownStore()
  const { darkTheme } = useThemeStore()
  const { tipActive, setTipActive } = useUiStore()
    
  const {width} = useWindowSize() 
  const isMobile = width < 1001
  
  


  useEffect( () => {
    if (groupDataValue) {
      setTipActive(false)
    } else {
      setTipActive(true)
    }
  }, [groupDataValue])



  return (
    <div className='main-content'>
      <div className={`schedule-wrap ${isMobile ? "mobile" : ""} ${darkTheme ? "dark" : ""}`}>
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
        
        </div>
        {!groupDataValue && (
          <Tip active={tipActive} />
        )}
        {groupDataValue && (
          <ScheduleContainer
            groupDataValue={groupDataValue}
            dateDataValue={dateDataValue}
            />
          )}
      </div>

      <NotificationOuter message={"домашнее задание сохранено."} type={'success'} />
    </div>
  )
}

export default MainContent
