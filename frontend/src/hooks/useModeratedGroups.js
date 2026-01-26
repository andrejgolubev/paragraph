import { useState, useEffect } from "react"
import API from "../api/API"
import { useAuthStore } from "../store/authStore"

const roleMap = {
  student: 'Студент', 
  admin: 'Администратор',
  teacher: 'Преподаватель',
}

export const useModeratedGroups = () => {
  const user = useAuthStore((state) => state.user) 
  const [moderatedGroups, setModeratedGroups] = useState([])
  const [displayRole, setDisplayRole] = useState('')


  // чтобы избежать лишних ререндеров
  useEffect(() => {
    API.getUserData().then( ({role}) => {
      if (role?.includes('admin')) {
        const moderatedGroups = role.split('.').slice(1,)
        setModeratedGroups(moderatedGroups)
        setDisplayRole(roleMap[role.split('.')[0]])
      } else {
        setDisplayRole(role ? roleMap[role] : '')
        setModeratedGroups([])
      }
    })
  }, [ user ])

  return { moderatedGroups, displayRole }
}