import Header from "./components/Header"
import Help from "./components/help-page/Help"
import ScheduleContent from "./components/ScheduleContent"
import { Provider } from "./context/Provider"
import { Route, Routes } from "react-router-dom"
import { Auth } from "./components/auth/Auth"

function App() {

  return (
    <Provider>
      <Header />
    
      <Routes>
        <Route path="/" element={<ScheduleContent />} />
        <Route path="/help" element={<Help />} />
        <Route path='/sign-in' element={<Auth type='sign-in' />} />
        <Route path='/sign-up' element={<Auth type='sign-up'/>} />
      </Routes>
    </Provider>
  )
}

export default App
