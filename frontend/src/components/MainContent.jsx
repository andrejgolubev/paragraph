import HomeworkModal from "./HomeworkModal"
import ScheduleContainer from "./ScheduleContainer"
import Dropdown from "./Dropdown"
import Tip from "./Tip"
import { useState, useEffect } from "react"

const MainContent = () => {
  const [tipActive, setTipActive] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => {
      setTipActive(true)
    }, 500)
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

      {/* <ScheduleContainer groupDataValue={1633} /> */}
      {/* notification outer */}
      {/* ... */}
    </div>
  )
}

export default MainContent
