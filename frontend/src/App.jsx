import Header from "./components/header/Header"
import Help from "./components/help-page/Help"
import ScheduleContent from "./components/main/ScheduleContent"
import Profile from "./components/profile/Profile"
import { Provider } from "./context/Provider"
import { Route, Routes } from "react-router-dom"
import { CookiesProvider } from "react-cookie"
import { AuthForm } from "./components/auth/AuthForm"

function App() {

  return (
    <CookiesProvider>
      <Provider>
        <Header />
      
        <Routes>
          <Route path="/" element={<ScheduleContent />} />
          <Route path="/help" element={<Help />} />
          <Route path='/sign-in' element={<AuthForm type='sign-in' />} />
          <Route path='/sign-up' element={<AuthForm type='sign-up'/>} />
          <Route path='/profile' element={<Profile />} />
        </Routes>
      </Provider>
    </CookiesProvider>
  )
}

export default App
