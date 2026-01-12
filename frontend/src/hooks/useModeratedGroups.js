import { useState, useEffect } from "react"
import homeworkAPI from "../api/homeworkAPI"
import { useAuthStore } from "../store/authStore"

export const useModeratedGroups = () => {
  const user = useAuthStore((state) => state.user) 
  const [moderatedGroups, setModeratedGroups] = useState([])
  const [displayRole, setDisplayRole] = useState('')

  const roleMap = {
    student: 'Студент', 
    admin: 'Администратор',
    teacher: 'Преподаватель',
  }

  // чтобы избежать лишних ререндеров
  useEffect(() => {
    homeworkAPI.getUserData().then( ({role}) => {
      if (role?.includes('admin')) {
        const moderatedGroups = role.split('.').slice(1,)
        console.log('moderatedGroups из useModeratedGroups:>> ', moderatedGroups);
        setModeratedGroups(moderatedGroups)
        setDisplayRole(roleMap[role.split('.')[0]])
      } else {
        setDisplayRole(role ? roleMap[role] : '')
        setModeratedGroups([])
      }
    })
  }, [ user?.role ])

  return { moderatedGroups, displayRole }
}