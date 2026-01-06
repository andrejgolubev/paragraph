import React, { useContext } from "react"
import { useLocation, Link } from "react-router-dom"
import { Context } from "../context/Provider"

export const NavItem = ({ children, path }) => {
  const {setLinksActive} = useContext(Context)
  const location = useLocation()


  return (
    <Link to={path} onClick={ () => setLinksActive( (prev) => !prev )}>
      <div className={`nav_item ${location.pathname === path ? "bold" : ""}`}>
        <p>{children}</p>
      </div>
    </Link>
  )
}
