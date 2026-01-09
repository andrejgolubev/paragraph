import { createContext, useEffect, useState } from "react"
import { useCookies } from "react-cookie"
import homeworkAPI from "../api/homeworkAPI"
import { useNavigate, useLocation } from "react-router-dom"

export const Context = createContext({})

export const Provider = ({ children }) => {

  const [linksActive, setLinksActive] = useState(false) // мобильное меню навигации

  


  // тема 
  const [darkTheme, setDarkTheme] = useState(() => {
    const saved = localStorage.getItem('darkTheme');
    return saved === 'true' ? true : false;
  });

  useEffect(() => {
    localStorage.setItem('darkTheme', darkTheme);
    
    if (darkTheme) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  }, [darkTheme]);



  // уведомления по типу "дз сохранено" , "успешный вход в аккаунт"
  const [notificationOuterMessage, setNotificationOuterMessage] = useState('')
  const [notificationOuterActive, setNotificationOuterActive] = useState(false)

  const [tipActive, setTipActive] = useState(false) //подсказка при первом заходе на сайт
  
  // клиентские куки
  const [groupDataValueCookies, setGroupDataValueCookies, removeGroupDataValueCookies] 
    = useCookies(
      ['group_data_value'], 
    )
  const groupDataValueCookie = groupDataValueCookies.groupDataValue
  const [groupDataValue, setGroupDataValue] = useState(groupDataValueCookie)

  const [dateDataValue, setDateDataValue] = useState("") // а дата кукам не подлежит
  

  // устанавливаем имя для ProfileDropdown используя access_token 
  const [username, setUsername] = useState('')
  const [userRole, setUserRole] = useState('')
  const [email, setEmail] = useState('')
  const [group, setGroup] = useState('')
  useEffect( () => {
    homeworkAPI.getUserData().then(resp => {
      if (resp?.status === 'ok') {
        setUsername(resp.username)
        setUserRole(resp.role)
        setEmail(resp.email)
        setGroup(resp.group)
      } else {
        setUsername('')
        setUserRole('')
        setEmail('')
        setGroup('')
      }
    })
  }, [notificationOuterActive, username]) // такая зависимость т.к. при входе в аккаунт срабатывает эта нотификэйшн


  // проверка на авторизацию при переходе на страницу профиля
  const navigate = useNavigate()
  const location = useLocation()
  const path = location.pathname.split('/').pop()
  
  useEffect(() => {
    const timer = setTimeout(() => {
      if (path === 'profile' && !username) {
        navigate('/sign-in')
      }
    }, 500)

    return () => clearTimeout(timer)
  }, [path, username])


  return (
    <Context.Provider
      value={{
        groupDataValue,
        setGroupDataValue,
        dateDataValue,
        setDateDataValue,
        //notificationOuter:
        notificationOuterActive, 
        setNotificationOuterActive,
        notificationOuterMessage, 
        setNotificationOuterMessage,
        // подсказка при первом входе:
        tipActive, 
        setTipActive,
        //клиентские куки:
        setGroupDataValueCookies,
        // имя профиля и роль доставаемая по access_token
        username, 
        userRole, 
        email,
        group,
        //theme:
        darkTheme, 
        setDarkTheme,
        //мобильная навигация: 
        linksActive,
        setLinksActive ,
      }}
    >
      {children}
    </Context.Provider>
  )
}
