import { useModeratedGroups } from "../../hooks/useModeratedGroups"
import React, { useRef, useCallback, useEffect, useState, useContext } from "react"
import { Link, replace, useNavigate } from "react-router-dom"
import { useForm } from "react-hook-form"
import { DevTool } from "@hookform/devtools"

import homeworkAPI from "../../api/homeworkAPI"
import {latinToCyrillic} from '../../utils/converters.js'
import NotificationOuter from '../notifications/NotificationOuter.jsx'
import { Context } from "../../context/Provider"

import user_icon from '../../images/auth/person.svg'
import group_icon from '../../images/auth/group.svg'
import password_icon from '../../images/auth/password.svg'
import email_icon from '../../images/auth/email.svg'




const Profile = () => {
  const { moderatedGroups, displayRole } = useModeratedGroups()
  
  const {
    darkTheme,
    username,
    userRole,
    email,
    group,
  } = useContext(Context)

  const navigate = useNavigate()

  const validationPreferences = {
    username: {
      minLength: 2,
      maxLength: 40,
      pattern: /^[a-zA-Zа-яА-Я\s\-]+$/,
    },
    email: {
      pattern: /^\S+@\S+\.\S+$/,
    },
    password: {
      // pattern: /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/,
      minLength: 8,
    }
  }
  
  const validateUsername = async (value) => {
    const username = value.trim()
    
    if (username.length < validationPreferences.username.minLength) {
      return `имя должно содержать минимум ${validationPreferences.username.minLength} символа`
    }
    
    if (username.length > validationPreferences.username.maxLength) {
      return `имя не должно превышать ${validationPreferences.username.maxLength} символов`
    }
    
    if (!validationPreferences.username.pattern.test(username)) {
      return "разрешены только буквы, пробелы и дефисы."
    }
    
    
    if (/\s{2,}/.test(username)) {
      return "нельзя использовать несколько пробелов подряд."
    }
    
    return true
  }

  const validatePassword = (pwd) => {
    
    const password = pwd.trim()

    if (password.length < validationPreferences.password.minLength) return 'пароль должен содержать минимум 8 символов.'
    
    if (!/[A-ZА-Я]/.test(password)) {
      return "пароль должен содержать хотя бы одну заглавную букву"
    }
    
    if (!/[a-zа-я]/.test(password)) {
      return "пароль должен содержать хотя бы одну строчную букву."
    }
    
    if (!/[0-9]/.test(password)) {
      return "пароль должен содержать хотя бы одну цифру."
    }
    
    if (!/[#?!@$%^&*-]/.test(password)) {
      return "пароль должен содержать хотя бы один специальный символ."
    }
    
    return true
  }
  
  const [submitMessageType, setSubmitMessageType] = useState('success')
  
  
  const form = useForm()
  const { register, control, handleSubmit, formState } = form
  const { errors } = formState
  
  const debounceTimerRef = useRef(null)

  const {setNotificationOuterActive, setNotificationOuterMessage} = useContext(Context)

  const handleProfileChange = (resp) => {
    setNotificationOuterMessage(resp.detail)
    if (resp.status === 'ok') {
      setSubmitMessageType('success') 
      
      // if (resp.type === 'sign-in') navigate('/', {replace: true}) // редирект на расписание если логин   
      // else navigate('/sign-in', {replace: true})  //редирект на логин если успешно зарегался
      // // имя и роль в ProfileDropdown устанавливаются через Provider
      // своя логика здесь ...

      setTimeout( async () => { 
        setNotificationOuterActive(true)
      }, 100)
      
    } else {
      setSubmitMessageType('error')
      setNotificationOuterActive(true)
    }
  }

  const onSubmit = ({email, password, username, group}) => {
    console.log('hi');
    // типа
    // homeworkAPI.sendProfileData(email, password, username, group).then(
      // resp => handleProfileChange(resp)
    // )
  }

  const groupAttemptsRef = useRef(0)

  const validateGroup = async (value) => {
    // если поле пустое, валидация проходит (поле опционально)
    if (!value || value.trim() === "") {
      return true
    }
    
    try {
      const groups = await homeworkAPI.getAllGroups()
      const groupExists = groups.some(
        (elem) => {
          const groupNumber = elem['group_number'] 
          return (
            groupNumber === value || 
            groupNumber === latinToCyrillic(value))
        }  

      )
      
      if (!groupExists) {
        groupAttemptsRef.current++
        return groupAttemptsRef.current < 5
          ? `группа не найдена, либо не существует.`
          : "введите группу в точности, как на официальном сайте расписания."
      }
      
      return true
    } catch (error) {
      console.error("Ошибка при проверке группы:", error)
      return "ошибка при проверке группы"
    }
  }

  const groupValidator = (value) => {
    if (!value?.trim()) {
      return true
    }

    // очищаем предыдущий таймер
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current)
    }

    return new Promise((resolve) => {
      debounceTimerRef.current = setTimeout(async () => {
        try {
          const result = await validateGroup(value)
          resolve(result)
        } catch (error) {
          resolve("ошибка при проверке группы")
        }
      }, 100)
    })
  } 

  useEffect(() => {
    return () => { // cleanup при размонтировании
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current)
      }
    }
  }, [])
  
  const requireText = 'это поле надо бы заполнить.'

  const darkOrNot = useRef('')
  darkOrNot.current = darkTheme? ' dark' : ''


  const usernameInputRef = useRef(null)
  const groupInputRef = useRef(null)
  const emailInputRef = useRef(null)
  const passwordInputRef = useRef(null)

  const focusInput = (inputRef) => {
    if (inputRef?.current) {
      inputRef.current.focus()
    }
  }

  // ДЛЯ ТОГО ЧТОБЫ ФОКУС СРАБАТЫВАЛ НЕ ТОЛЬКО ПРИ КЛИКЕ НЕПОСРЕДСТВЕННО НА INPUT: 
  // сохраняем register поля, чтобы привязать ref и к react-hook-form форме, и к нашим refs
  // в usernameField, groupField, emailField, passwordField будет сохранен обьект вида 
  // { onChange, onBlur, ref, name, ... }

  const usernameField = register("username", {
      required: requireText, 
      validate: {
        validFormat: async (value) => validateUsername(value)
      }
    }) 

  const groupField = register("group", {
      validate: {
        validateGroup: (value) => groupValidator(value)
      }
    }) 

  const emailField = register("email", {
    required: requireText, 
    pattern: {
      value: validationPreferences.email.pattern,
      message: "неправильный формат электронной почты."
    }, 
  })

  const passwordField = register("password", {
    required: requireText,
    validate: (value) => validatePassword(value)
  })


  return (
    <div className={`profile${darkOrNot.current}`}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="profile__header">
          <div className="profile__header__text">профиль</div>
        </div>
        <div className="profile__inputs">
          <div className="username-block">
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
                defaultValue={username}
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
                placeholder="группа"
                defaultValue={group}
              />
            <p className='profile__error'>{errors.group?.message}</p>
            </div>
          </div>
          <div className="email-block">
            <label htmlFor="email">эл. почта</label>
            <div
              className={`input-div${darkOrNot.current} email-input`}
              onClick={() => focusInput(emailInputRef)}
            >
              <input
                {...emailField}
                ref={(el) => {
                  emailField.ref(el)
                  emailInputRef.current = el
                }}
                className={`input${darkOrNot.current}`}
                type="email"
                id="email"
                defaultValue={email}
              />
                <p className='profile__error'>{errors.email?.message}</p>
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
                defaultValue='abracadabra!'
              />
              <p className='profile__error'>{errors.password?.message}</p>
            </div>
          </div>
        </div>
        
        <div className="profile__submit">
          <button className={`profile__submit__btn${darkOrNot.current}`}>сохранить</button>
        </div>
      </form>
    </div>
  
  )
};

export default Profile;