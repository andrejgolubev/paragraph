import { createContext, useEffect, useState } from "react"
import { useCookies } from "react-cookie"
import homeworkAPI from "../api/homeworkAPI"


export const Context = createContext({})

export const Provider = ({ children }) => {
  // тема 
  const [darkTheme, setDarkTheme] = useState(() => {
    const saved = localStorage.getItem('darkTheme');
    return saved === 'true' ? true : false;
  });

  useEffect(() => {
    // Сохраняем тему в localStorage
    localStorage.setItem('darkTheme', darkTheme);
    
    // Меняем background
    if (darkTheme) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  }, [darkTheme]);

  const toggleTheme = () => {
    setDarkTheme(!darkTheme);
  };



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
  
  useEffect( () => {
    homeworkAPI.getUserData().then(resp => {
      setUsername(resp.username)
      setUserRole(resp.role)
    })
  }, [notificationOuterActive]) // такая зависимость т.к. при входе в аккаунт срабатывает эта нотификэйшн

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
        //
        tipActive, 
        setTipActive,
        setGroupDataValueCookies,
        username, 
        setUsername, 
        userRole, 
        setUserRole,
        //theme:
        darkTheme, 
        setDarkTheme,
        toggleTheme,
      }}
    >
      {children}
    </Context.Provider>
  )
}
