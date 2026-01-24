import React, { useRef, useEffect, useState } from "react"
import { useNavigate, useLocation } from "react-router-dom"
import { useForm } from "react-hook-form"

import { useModeratedGroups } from "../../hooks/useModeratedGroups"
import API, {showNotificationOuter} from "../../api/API"
import NotificationOuter from "../notifications/NotificationOuter.jsx"

import pencilIcon from "../../images/profile/profile-page/pencil.svg"
import pencilIconActive from "../../images/profile/profile-page/pencil-active.svg"
import pencilIconDark from "../../images/profile/profile-page/pencil-dark.svg"
import pencilIconActiveDark from "../../images/profile/profile-page/pencil-dark-active.svg"

import { useWindowSize } from "../../hooks/useWindowSize"
import { validationPreferences } from "../../config/settings.js"
import { useThemeStore } from "../../store/themeStore"
import { useAuthStore } from "../../store/authStore"


const Profile = () => {
  const { darkTheme } = useThemeStore()
  const {user, fetchUser} = useAuthStore()

  if (!user) return <div className="profile"><p>пожалуйста, авторизуйтесь. перенаправляю на страницу входа...</p></div>

  const {width} = useWindowSize()
  
  const { moderatedGroups, displayRole } = useModeratedGroups()

  
  const validateUsername = async (value) => {
    const username = value.trim()
    
    if (username.length < validationPreferences.username.minLength) {
      return `имя должно содержать минимум ${validationPreferences.username.minLength} символа`
    }
    
    if (username.length > validationPreferences.username.maxLength) {
      return `имя не должно превышать ${validationPreferences.username.maxLength} символов`
    }
    
    if (!validationPreferences.username.pattern.test(username)) {
      return "имя содержит недопустимые символы."
    }
    
    if (/\s{2,}/.test(username)) {
      return "нельзя использовать несколько пробелов подряд."
    }
    
    return true
  }

  
  
  const form = useForm({
    defaultValues: {
      username: user?.username,
      group: user?.group,
      email: user?.email,
      password: '***********',
    },
    values: {
      username: user?.username,
      group: user?.group,
      email: user?.email,
      password: '***********',
    },
  })

  const { register, handleSubmit, formState } = form
  const { errors } = formState
  
  const debounceTimerRef = useRef(null)
  
  
  const onSubmit = ({password, username, group}) => {
    API.updateUserData({email: user?.email, password, username, group}).then(
      resp => {
        if (resp.status === 'ok') {
          fetchUser()
          setIsEditable(false)
          showNotificationOuter(resp.detail , 'success')
        } else {
          showNotificationOuter(resp.detail , 'error')
        }
      }
    )
  }

  
  const validateGroup = (value) => {
    if (!value?.trim()) return true
  }

  useEffect(() => {
    return () => { // cleanup при размонтировании
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current)
      }
    }
  }, [])
  

  const darkOrNot = useRef('')
  darkOrNot.current = darkTheme? ' dark' : ''


  const usernameInputRef = useRef(null)
  const groupInputRef = useRef(null)
  const emailInputRef = useRef(null)
  const passwordInputRef = useRef(null)

  const focusInput = (inputRef) => {
    if (inputRef?.current) {
      const currentInput = inputRef.current
      currentInput.focus()
      // const len = currentInput.value.length
      // currentInput.setSelectionRange(len, len)
    } else return
  }

  // ДЛЯ ТОГО ЧТОБЫ ФОКУС СРАБАТЫВАЛ НЕ ТОЛЬКО ПРИ КЛИКЕ НЕПОСРЕДСТВЕННО НА input: 
  // сохраняем register поля, чтобы привязать ref и к react-hook-form форме, и к нашим refs
  // в usernameField, groupField, passwordField будет сохранен обьект вида 
  // { onChange, onBlur, ref, name, ... }
  const usernameField = register("username", {
      required: false, 
      validate: {
        validFormat: async (value) => validateUsername(value)
      },
    }) 

  const groupField = register("group", {
    required: false,
      validate: {
        validateGroup: (value) => validateGroup(value)
      }, 
    }) 

  const passwordField = register("password", {
    required: true,
    // // не нужно validate, так как не обновляем пароль, а только проверяем его 
  })

  


  const [isEditable, setIsEditable] = useState(false)

  useEffect(() => {
    if (isEditable) focusInput(usernameInputRef)
    else form.reset()
  }, [isEditable])


  const handleImmutableFieldClick = (message) => {
    if (!isEditable) return
    showNotificationOuter(message , 'error')    
  }

  // если isEditable был false (т.е. нажали на кнопку редактировать), 
  // то скроллим вниз на кнопку сохранить (для десктопа), а затем меняем его на true
  const handleToggleEditing = () => {
    setIsEditable((prev) => {
      if (!prev) { 
        passwordInputRef.current.value = ''
        setTimeout(() => {
          // только для десктопа, чтобы скролл не сработал на мобилке. на мобилке только фокус на поле ввода.
          if (width > 1100) saveButtonRef.current?.scrollIntoView({ behavior: 'smooth' })
        }, 100)
      } 
      return !prev
    })
  }


  const navigate = useNavigate()
  const location = useLocation()
  const path = location.pathname.split('/').pop()

  const handleLogout = () => {
    if (path === 'profile') {
      navigate('/sign-in')
    }
    API.logout().then( resp => {
      showNotificationOuter(resp.detail, 'error')
      fetchUser()
    })
  }

  const saveButtonRef = useRef(null)

  return (
    <div className={`profile${darkOrNot.current} ${isEditable? 'editing' : ''}`}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="profile__header">
          <div className="profile__header__text">профиль</div>
          <div className="profile__header__pencil" onClick={handleToggleEditing}>
            <img
              className="profile__header__pencil__icon"
              src={darkTheme? (isEditable? pencilIconActiveDark : pencilIconDark) : (isEditable? pencilIconActive : pencilIcon)}
              title="редактировать профиль"
            />
          </div>
        </div>
        <div className="profile__inputs">
          <div className="username-block" >
            <label htmlFor="username">имя</label>
            <div
              className={`input-div${darkOrNot.current}`}
              onClick={() => focusInput(usernameInputRef)}
            >
              <input
                {...usernameField}
                ref={(el) => {
                  usernameField.ref(el)
                  usernameInputRef.current = el
                }}
                className={`input${darkOrNot.current}`}
                type="text"
                id="username"
                readOnly={!isEditable}
              />
              <p className='profile__error'>{errors.username?.message}</p>
            </div>
          </div>

          <div className="group-block">
            <label htmlFor="group">группа</label>
            <div
              className={`input-div${darkOrNot.current}`}
              onClick={() => focusInput(groupInputRef)}
            >
              <input
                {...groupField}
                ref={(el) => {
                  groupField.ref(el)
                  groupInputRef.current = el
                }}
                className={`input${darkOrNot.current}`}
                type="text"
                id="group"
                placeholder="не указана"
                readOnly={!isEditable}
              />
            <p className='profile__error'>{errors.group?.message}</p>
            </div>
          </div>

          <div className="role-block" onClick={() => handleImmutableFieldClick('самому себе роль изменять нельзя :(')}>
            <label htmlFor="role">роль</label>
            <div 
              className={`input-div${darkOrNot.current} immutable-field`}
            >
              {displayRole.toLowerCase() === 'администратор'
                  ? <p>{`${displayRole} (${moderatedGroups})`}</p> 
                  : <p>{displayRole}</p>}
            </div>
          </div>

          <div className="email-block" onClick={() => handleImmutableFieldClick('электронную почту изменять нельзя :(')}>
            <label htmlFor="role">эл. почта</label>
            <div
              className={`input-div${darkOrNot.current} immutable-field`}
            >
              <p>{user?.email}</p>
            </div>
          </div>
          
          <div className="pwd-block">
            <label htmlFor="password">пароль</label>
            <div
              className={`input-div${darkOrNot.current} pwd-input`}
              onClick={() => focusInput(passwordInputRef)}
            >
              <input
                {...passwordField}
                ref={(el) => {
                  passwordField.ref(el)
                  passwordInputRef.current = el
                }}
                className={`input${darkOrNot.current}`}
                type="password"
                id="password"
                placeholder="для применения правок..."
                readOnly={!isEditable}
              />
              <p className='profile__error'>{errors.password?.message}</p>
            </div>
            { isEditable ? (
            <div className="profile__submit">
              <button className={`profile__submit__cancel__btn${darkOrNot.current}`} onClick={handleToggleEditing}>отмена</button>
              <button className={`profile__submit__save__btn${darkOrNot.current}`} type="submit" ref={saveButtonRef}>сохранить</button>
            </div>
            ):(
              <div className="profile__submit">
                <div className="profile__submit__logout-wrap">
                  <button
                    type="button"
                    className={`profile__submit__logout__btn${darkOrNot.current}`}
                    onClick={handleLogout}
                  >
                    выйти из аккаунта
                  </button>
                </div>
              </div>
            )}
          </div>

        </div>
        <NotificationOuter />
        
      </form>
    </div>
  
  )
}

export default Profile