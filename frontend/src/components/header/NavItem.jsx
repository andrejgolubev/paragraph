import React from "react"
import { useLocation, Link } from "react-router-dom"
import { useUiStore } from "../../store/uiStore"

export const NavItem = ({ children, path }) => {
  const setLinksActive = useUiStore((state) => state.setLinksActive)
  const location = useLocation()


  return (
    <Link to={path} onClick={ () => setLinksActive( (prev) => !prev )}>
      <div className={`nav_item ${location.pathname === path ? "bold" : ""}`}>
        <p>{children}</p>
      </div>
    </Link>
  )
}
