import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { Mosaic } from 'react-loading-indicators'
import { useThemeStore } from '../store/themeStore'
import { useRef } from 'react'

export const ProtectedRoute = ({ children, type }) => {
  const {darkTheme} = useThemeStore()
  
  
  const user = useAuthStore((state) => state.user)
  const loading = useAuthStore((state) => state.loading)
  const location = useLocation()

  const statement = useRef(false)
  const navTo = useRef('')

  if (type === 'profile') {
    statement.current = !user && !loading
    navTo.current = '/sign-in'
  } else if (type === 'auth') {
    statement.current = user && !loading
    navTo.current = '/'
  }

  if (statement.current) {
    return <Navigate to={navTo.current} state={{ from: location }} replace />
  } else if (loading) {
    return (
    <div className="loading-indicator">
      <Mosaic
        color={darkTheme? '#d2d2d2' : '#fff'}
        size="large"
        text="загрузка..."
        textColor="#CBCBDE"
      />
    </div>)
  }

  return children
}