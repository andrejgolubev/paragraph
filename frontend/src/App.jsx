import { useContext } from "react"
import Header from "./components/Header"
import Help from "./components/help-page/Help"
import ScheduleContent from "./components/ScheduleContent"
import { Context, Provider } from "./context/Provider"
import { Route, Routes } from "react-router-dom"

function App() {

  return (
    <Provider>
      <Header />

      <Routes>
        <Route path="/" element={<ScheduleContent />} />
        <Route path="/help" element={<Help />} />
      </Routes>
    </Provider>
  )
}

export default App
