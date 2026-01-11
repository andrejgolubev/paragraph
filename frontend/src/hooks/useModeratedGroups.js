import { useState, useEffect, useContext } from "react"
import homeworkAPI from "../api/homeworkAPI"
import { Context } from "../context/Provider"

export const useModeratedGroups = () => {
  const {userRole} = useContext(Context)
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
  }, [ userRole ])

  return { moderatedGroups, displayRole }
}