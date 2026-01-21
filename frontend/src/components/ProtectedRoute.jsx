import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { Mosaic } from 'react-loading-indicators'
import { useThemeStore } from '../store/themeStore'
import { useEffect } from 'react'

export const ProtectedRoute = ({ children, type }) => {
  const darkTheme = useThemeStore( (state) => state.darkTheme)
  const {user, fetchUser, loading} = useAuthStore.getState()
  const location = useLocation()
  
  useEffect(() => {
    fetchUser()
  }, [])

  const isAuthenticated = Boolean(user)
  const isChecking = loading

  if (isChecking) {
    return (
      <div className="loading-indicator">
        <Mosaic
          color={darkTheme ? '#d2d2d2' : '#fff'}
          size="large"
          text="загрузка..."
          textColor="#CBCBDE"
        />
      </div>
    )
  }

  if (type === 'profile' && !isAuthenticated) {
    return <Navigate to="/sign-in" state={{ from: location }} replace />
  }

  if (type === 'auth' && isAuthenticated) {
    return <Navigate to="/" replace />
  }

  return children
}