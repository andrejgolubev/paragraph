import HomeworkModal from "./HomeworkModal"
import ScheduleContainer from "./ScheduleContainer"
import Dropdown from "./Dropdown"
import Tip from "./Tip"
import { useState, useEffect, useContext } from "react"
import { Context } from "../context/Provider"
import { Mosaic } from "react-loading-indicators"
import NotificationOuter from "./notifications/NotificationOuter"

const MainContent = () => {
  const [tipActive, setTipActive] = useState(false)
  const { groupDataValue, dateDataValue } = useContext(Context)

  useEffect(() => {
    const timer = setTimeout(() => {
      setTipActive(true)
    }, 100)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="main-content">
      <div className="options">
        <Dropdown
          name={"group"}
          func={"search"}
          placeholder={"номер группы"}
          readOnly={false}
          setTipActive={setTipActive}
        />
        <Dropdown
          name={"week"}
          func={"select"}
          placeholder={"дата/неделя"}
          readOnly={true}
          setTipActive={setTipActive}
        />
        <div className="corpuses">
          <p>C - Центральный корпус⠀⠀⠀⠀B - Бизнес-инкубатор</p>
          <p>L - Лабораторный корпус ⠀⠀⠀F - Первый корпус</p>
        </div>
      </div>
      <Tip active={tipActive} />

      {groupDataValue && (
        <ScheduleContainer
          groupDataValue={groupDataValue}
          dateDataValue={dateDataValue}
        />
      )}

      <NotificationOuter message={"домашнее задание сохранено."} />
      {/* ... */}
    </div>
  )
}

export default MainContent
