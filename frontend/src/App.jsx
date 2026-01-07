import Header from "./components/header/Header"
import Help from "./components/help-page/Help"
import ScheduleContent from "./components/ScheduleContent"
import Profile from "./components/profile/Profile"
import { Provider } from "./context/Provider"
import { Route, Routes } from "react-router-dom"
import { Auth } from "./components/auth/Auth"
import { CookiesProvider } from "react-cookie"

function App() {

  return (
    <CookiesProvider>
      <Provider>
        <Header />
      
        <Routes>
          <Route path="/" element={<ScheduleContent />} />
          <Route path="/help" element={<Help />} />
          <Route path='/sign-in' element={<Auth type='sign-in' />} />
          <Route path='/sign-up' element={<Auth type='sign-up'/>} />
          <Route path='/profile' element={<Profile />} />
        </Routes>
      </Provider>
    </CookiesProvider>
  )
}

export default App
