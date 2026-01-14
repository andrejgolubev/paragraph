import Header from "./components/header/Header"
import Help from "./components/help-page/Help"
import MainContent from "./components/main/MainContent"
import Profile from "./components/profile/Profile"
import { Provider } from "./context/Provider"
import { Route, Routes } from "react-router-dom"
import { AuthForm } from "./components/auth/AuthForm"
import News from "./components/News"
import { ProtectedRoute } from "./components/ProtectedRoute"


function App() {
  

  return (
    <Provider>
      <Header />

      <Routes>
        <Route path="/" element={<MainContent />} />
        <Route path="/news" element={<News />} />
        <Route path="/help" element={<Help />} />
        <Route path='/sign-in' element={
          <ProtectedRoute type='auth'> <AuthForm type='sign-in' /> </ProtectedRoute>
          } />
        <Route path='/sign-up' element={
          <ProtectedRoute type='auth'> <AuthForm type='sign-up'/> </ProtectedRoute>
          } />
        <Route path='/profile' element={
          <ProtectedRoute type='profile'> <Profile /> </ProtectedRoute>
          } />
      </Routes>
    </Provider>
  )
}

export default App
