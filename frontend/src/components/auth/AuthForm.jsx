import React, { useRef, useEffect, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useForm } from "react-hook-form"
import { DevTool } from "@hookform/devtools"

import API from "../../api/API"
import NotificationOuter from "../notifications/NotificationOuter.jsx"

import user_icon from "../../images/auth/person.svg"
import group_icon from "../../images/auth/group.svg"
import password_icon from "../../images/auth/password.svg"
import email_icon from "../../images/auth/email.svg"

import { validationPreferences } from "../../config/settings.js"

import { useThemeStore } from "../../store/themeStore"
import { useUiStore } from "../../store/uiStore"
import { useAuthStore } from "../../store/authStore"



export const AuthForm = ({ type }) => {
  const { darkTheme } = useThemeStore()
  const fetchUser = useAuthStore((state) => state.fetchUser)
  const navigate = useNavigate()

  const validateUsername = async (value) => {
    const username = value.trim()

    if (username.length < validationPreferences.username.minLength) {
      return `имя должно содержать минимум ${validationPreferences.username.minLength} символа`
    }

    if (username.length > validationPreferences.username.maxLength) {
      return `имя не должно превышать ${validationPreferences.username.maxLength} символов`
    }

    if (!validationPreferences.username.pattern.test(username)) {
      return "используйте кириллицу, пробелы, точки и дефисы."
    }

    if (/\s{2,}/.test(username)) {
      return "нельзя использовать несколько пробелов подряд."
    }

    return true
  }

  const validatePassword = (pwd) => {
    if (type === "sign-in") return true // чтоб не бесили уведы про валидацию когда входишь в акк

    const password = pwd.trim()

    if (password.length < validationPreferences.password.minLength)
      return "пароль должен содержать минимум 8 символов."

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

  let authType = "",
    authTitle = ""

  const [submitMessageType, setSubmitMessageType] = useState("")

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

  

  const {
    setNotificationOuterActive,
    setNotificationOuterMessage,
    setNotificationOuterType
  } = useUiStore.getState()

  const handleAuth = (resp) => {
    setNotificationOuterMessage(resp.detail)
    if (resp.status === "ok") {
      setSubmitMessageType("success")
      setNotificationOuterType('success')
      if (resp.type === "sign-in") {
        fetchUser()
        navigate("/", { replace: true }) // редирект на расписание если логин
      } 
      else navigate("/sign-in", { replace: true }) // редирект на логин если успешно зарегался

      setTimeout(async () => {
        setNotificationOuterActive(true)
      }, 100)
    } 
    else {
      setSubmitMessageType("error")
      setNotificationOuterType('error')
      setNotificationOuterActive(true)
    }
  }

  const onSubmit = (data) => {
    if (type === "sign-up") {
      const { email, password, username, group, acceptPd, acceptTerms } = data
      API
        .sendRegisterData(email, password, username, group, acceptPd, acceptTerms)
        .then((resp) => handleAuth(resp))
    } else if (type === "sign-in") {
      const { email, password } = data
      API
        .sendLoginData(email, password)
        .then((resp) => handleAuth(resp))
    }
  }

  const validateGroup = (value) => {
    if (!value?.trim()) return true
  }

  useEffect(() => {
    return () => {
      // cleanup при размонтировании
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current)
      }
    }
  }, [])

  const requireText = "это поле надо бы заполнить."

  const darkOrNot = useRef("")
  darkOrNot.current = darkTheme ? " dark" : ""

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

  let usernameField = null,
    groupField = null

  if (type === "sign-up") {
    usernameField = register("username", {
      required: requireText,
      validate: {
        validFormat: async (value) => validateUsername(value),
      },
    })
    groupField = register("group", {
      validate: {
        validateGroup: (value) => validateGroup(value),
      },
    })
  }

  const emailField = register("email", {
    required: requireText,
    pattern: {
      value: validationPreferences.email.pattern,
      message: "неправильный формат электронной почты.",
    },
  })

  const passwordField = register("password", {
    required: requireText,
    validate: (value) => validatePassword(value),
  })

  return (
    <div className={`auth${darkOrNot.current}`}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="auth__header">
          <div className="auth__header__text">{authTitle}</div>
        </div>
        <div className="auth__inputs">
          {type === "sign-up" && usernameField && groupField && (
            <>
              <div
                className={`input-div${darkOrNot.current}`}
                onClick={() => focusInput(usernameInputRef)}
              >
                <img src={user_icon} alt="user icon" />
                <input
                  {...usernameField}
                  ref={(el) => {
                    usernameField.ref(el)
                    usernameInputRef.current = el
                  }}
                  className={`input${darkOrNot.current}`}
                  type="text"
                  id="username"
                  placeholder="имя"
                  autoComplete="username"
                />
                <p className="auth__error">{errors.username?.message}</p>
              </div>
              <div
                className={`input-div${darkOrNot.current}`}
                onClick={() => focusInput(groupInputRef)}
              >
                <img src={group_icon} alt="user icon" />
                <input
                  {...groupField}
                  ref={(el) => {
                    groupField.ref(el)
                    groupInputRef.current = el
                  }}
                  className={`input${darkOrNot.current}`}
                  type="text"
                  id="group"
                  placeholder="группа (необяз.)"
                  autoComplete="group"
                />
                <p className="auth__error">{errors.group?.message}</p>
              </div>
            </>
          )}
          <div
            className={`input-div${darkOrNot.current} email-input`}
            onClick={() => focusInput(emailInputRef)}
          >
            <img src={email_icon} alt="email icon" />
            <input
              {...emailField}
              ref={(el) => {
                emailField.ref(el)
                emailInputRef.current = el
              }}
              className={`input${darkOrNot.current}`}
              type="email"
              id="email"
              placeholder="эл. почта"
              autoComplete="email"
            />
            <p className="auth__error">{errors.email?.message}</p>
          </div>
          <div className="pwd-block">
            <div
              className={`input-div${darkOrNot.current} pwd-input`}
              onClick={() => focusInput(passwordInputRef)}
            >
              <img src={password_icon} alt="password icon" />
              <input
                {...passwordField}
                ref={(el) => {
                  passwordField.ref(el)
                  passwordInputRef.current = el
                }}
                className={`input${darkOrNot.current}`}
                type="password"
                id="password"
                placeholder="пароль"
                autoComplete="password"
              />
              <p className="auth__error">{errors.password?.message}</p>
            </div>
            {/* {type === "sign-in" && (
              <div className="forgot-password">
                <span>забыли пароль?</span>
              </div>
            )} */}




            
          </div>

          {type === "sign-up" && (
            <div className={`checkbox-block${darkOrNot.current}`}>
              {/* Чекбокс 1 */}
              <div className="checkbox-block__checkbox">
                <label className="checkbox-block__checkbox__label">
                  <input
                    type="checkbox"
                    {...register("acceptPd", {
                      required: "Необходимо дать согласие на обработку ПД",
                    })}
                  />
                  <span className="checkbox__text">
                    Я даю{" "}
                    <Link to="/pd" target="_blank">
                      согласие на обработку персональных данных
                    </Link>
                  </span>
                </label>
                {errors.acceptPd && (
                  <p className="checkbox-block__checkbox__error">
                    <span>{errors.acceptPd.message}</span>
                  </p>
                )}
              </div>

              {/* Чекбокс 2 */}
              <div className="checkbox-block__checkbox">
                <label className="checkbox-block__checkbox__label">
                  <input
                    type="checkbox"
                    {...register("acceptTerms", {
                      required:
                        "Необходимо принять вышеуказанные документы",
                    })}
                  />
                  <span className="checkbox-block__checkbox__text">
                    Я принимаю{" "}
                    <Link to="/terms" target="_blank">
                      пользовательское соглашение
                    </Link>{" "}
                    и
                    <Link to="/privacy" target="_blank">
                      {" "}
                      политику конфиденциальности
                    </Link>
                  </span>
                </label>
                {errors.acceptTerms && (
                  <p className="checkbox-block__checkbox__error">
                    <span>{errors.acceptTerms.message}</span>
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
        <div className="auth__submit">
          <button className={`auth__submit__btn${darkOrNot.current}`}>
            {authType}
          </button>
        </div>
        {type === "sign-in" ? (
          <Link to="/sign-up">
            <div className="alternative-text">
              нет аккаунта? <span>зарегистируйтесь</span>
            </div>
          </Link>
        ) : (
          <Link to="/sign-in">
            <div className="alternative-text">
              уже есть аккаунт? <span>войдите</span>
            </div>
          </Link>
        )}
      </form>
      <NotificationOuter type={submitMessageType} />
      <DevTool control={control} />
    </div>
  )
}
