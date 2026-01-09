import ScheduleContainer from "./ScheduleContainer" // раньше был MainContent
import Dropdown from "./Dropdown"
import Tip from "../main/Tip"
import { useEffect, useContext } from "react"
import { Context } from "../../context/Provider"
import NotificationOuter from "../../components/notifications/NotificationOuter"
import { useWindowSize } from "../../hooks/useWindowSize"

const ScheduleContent = () => {
  const { groupDataValue, dateDataValue, tipActive, setTipActive } = useContext(Context)
  
  if (groupDataValue) setTipActive(false)

  useEffect( () => {
    setTipActive(true)
  }, [])

  const {width} = useWindowSize() 
  const isMobile = width < 600


  return (
    <div className='main-content'>
      <div className="options">
        <Dropdown
          name={"group"}
          func={"search"}
          placeholder={"номер группы"}
          readOnly={false}
        />
        <Dropdown
          name={"week"}
          func={"select"}
          placeholder={"дата/неделя"}
          readOnly={true}
        />

        <div className="corpuses">
          <p>C - Центральный корпус⠀⠀⠀⠀B - Бизнес-инкубатор</p>
          <p>L - Лабораторный корпус ⠀⠀⠀F - Первый корпус</p>
        </div>
      </div>
      {/* <Tip active={tipActive} /> */}

      {groupDataValue && (
        <ScheduleContainer
          groupDataValue={groupDataValue}
          dateDataValue={dateDataValue}
          />
        )}

      <NotificationOuter message={"домашнее задание сохранено."} type={'success'} />
    </div>
  )
}

export default ScheduleContent
