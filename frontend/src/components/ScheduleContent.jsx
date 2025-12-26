import ScheduleContainer from "./ScheduleContainer" // раньше был MainContent
import Dropdown from "./Dropdown"
import Tip from "./Tip"
import { useState, useEffect, useContext } from "react"
import { Context } from "../context/Provider"
import NotificationOuter from "./notifications/NotificationOuter"

const ScheduleContent = () => {
  const { groupDataValue, dateDataValue, tipActive, setTipActive } = useContext(Context)

  useEffect( () => {
      setTipActive(true)
  }, [])

  if (groupDataValue) {
    setTipActive(false)
  } 

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

export default ScheduleContent
