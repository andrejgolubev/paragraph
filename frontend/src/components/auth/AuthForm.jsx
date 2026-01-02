import React, { useRef, useCallback, useEffect, useState, useContext } from "react"
import { Link, replace, useNavigate } from "react-router-dom"
import { useForm } from "react-hook-form"
import { DevTool } from "@hookform/devtools"

import homeworkAPI from "../../api/homeworkAPI"
import {latinToCyrillic} from '../../utils/converters.js'
import NotificationOuter from '../notifications/NotificationOuter.jsx'
import { Context } from "../../context/Provider"

import user_icon from "../../images/auth/person.svg"
import group_icon from "../../images/auth/group.svg"
import password_icon from "../../images/auth/password.svg"
import email_icon from "../../images/auth/email.svg"

export const AuthForm = ({ type }) => {

  const navigate = useNavigate()


  // будет переменная userAuthorized с СОСТОЯНИЕМ от которой будет зависеть type
  // так что такя реализация с let допустима
  let authType = ""
  let authTitle = ""
  // const [submitMessage, setSubmitMessage] = useState('')
  const [submitMessageType, setSubmitMessageType] = useState('success')

  if (type === "sign-up") {
    authType = "зарегистироваться"
    authTitle = "регистрация"
  } else if (type === "sign-in") {
    authType = "войти"
    authTitle = "добро пожаловать!"
  }

  
  const form = useForm()
  const { register, control, handleSubmit, formState } = form
  const { errors } = formState
  
  const debounceTimerRef = useRef(null)

  const {notificationOuterActive, setNotificationOuterActive, setNotificationOuterMessage} = useContext(Context)

  const handleAuth = (resp) => {
    setNotificationOuterMessage(resp.detail)
    if (resp.status === 'ok') {
      setSubmitMessageType('success') 
      
      if (resp.type === 'sign-in') navigate('/', {replace: true}) // редирект на расписание если логин   
      else navigate('/sign-in', {replace: true})  //редирект на логин если успешно зарегался
      // имя и роль в ProfileDropdown устанавливаются через Provider

      setTimeout( async () => { 
        setNotificationOuterActive(true)
      }, 100)
      
      
      
    } else {
      setSubmitMessageType('error')
      setNotificationOuterActive(true)
    }
  }

  const onSubmit = ({email, password, username, group}) => {
    if (type === 'sign-up') {
      homeworkAPI.sendRegisterData(email, password, username, group).then(
        resp => handleAuth(resp)
      )
        
    } else if (type === 'sign-in') {
      homeworkAPI.sendLoginData(email, password).then(
        resp => handleAuth(resp)
      )
    } else {
      console.log('Указан неверный тип формы');
    }
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
        groupAttemptsRef.current ++
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
    if (!value.trim()) {
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

  return (
    <div className="auth">
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="auth__header">
          <div className="text">{authTitle}</div>
        </div>
        <div className="auth__inputs">
          {type === "sign-up" && (
            <>
              <div className="input">
                <img src={user_icon} alt="user icon" />
                <input
                  type="text"
                  id="username"
                  placeholder="имя"
                  {...register("username", {
                    required: requireText
                  })}
                />
                <p className='auth__error'>{errors.username?.message}</p>
              </div>
              <div className="input">
                <img src={group_icon} alt="user icon" />
                <input
                  type="text"
                  id="group"
                  placeholder="группа (опционально)"
                  {...register("group", 
                    {
                      validate: {
                        validateGroup: (value) => groupValidator(value)
                      }
                  }
                )}
                />
                <p className='auth__error'>{errors.group?.message}</p>
              </div>
            </>
          )}
          <div className="input">
            <img src={email_icon} alt="email icon" />
            <input
              type="email"
              id="email"
              placeholder="электронная почта"
              {...register("email", {
                required: requireText, 
                pattern: {
                  value: /^\S+@\S+\.\S+$/,
                  message: "неправильный формат электронной почты."
                }, 
                // validate : обязательно валидация !! 
              })}
              />
              <p className='auth__error'>{errors.email?.message}</p>
          </div>
          <div className="input">
            <img src={password_icon} alt="password icon" />
            <input
              type="password"
              id="password"
              placeholder="пароль"
              {...register("password", {
                required: requireText
              }) }
            />
            <p className='auth__error'>{errors.password?.message}</p>
          </div>
        </div>
        {type === "sign-in" && (
          <div className="forgot-password">
            <span>забыли пароль?</span>
          </div>
        )}
        <div className="auth__submit">
          <button className="auth__submit__btn">{authType}</button>
        </div>
        {type === "sign-in" ? (
          <Link to="/sign-up">
            <div>
              нет аккаунта? <span>зарегистируйтесь</span>
            </div>
          </Link>
        ) : (
          <Link to="/sign-in">
            <div>
              уже есть аккаунт? <span>войдите</span>
            </div>
          </Link>
        )}
      </form>
      <NotificationOuter 
      type={submitMessageType}
      />
      <DevTool control={control} />
    </div>
  )
}
