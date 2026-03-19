import React, { useRef, useEffect, useState } from "react"
import { useNavigate, useLocation } from "react-router-dom"
import { useForm } from "react-hook-form"

import API, { showNotificationOuter } from "../../api/API"

import pencilIcon from "../../images/profile/profile-page/pencil.svg"
import pencilIconActive from "../../images/profile/profile-page/pencil-active.svg"
import pencilIconDark from "../../images/profile/profile-page/pencil-dark.svg"
import pencilIconActiveDark from "../../images/profile/profile-page/pencil-dark-active.svg"

import { useModeratedGroups } from "../../hooks/useModeratedGroups"
import { useWindowSize } from "../../hooks/useWindowSize"
import { validationPreferences } from "../../config/settings.js"
import { useThemeStore } from "../../store/themeStore"
import { useAuthStore } from "../../store/authStore"

const Profile = () => {
  const darkTheme = useThemeStore((state) => state.darkTheme)
  const { user, fetchUser } = useAuthStore()
  const { width } = useWindowSize()
  const { moderatedGroups, displayRole } = useModeratedGroups()


  const form = useForm({
    values: {
      username: user?.username,
      group: user?.group,
      email: user?.email,
      password: "***********",
    },
    defaultValues: {
      username: user?.username,
      group: user?.group,
      email: user?.email,
      password: "***********",
    },
  })

  const { register, handleSubmit, formState } = form
  const { errors } = formState


  useEffect(() => {
    if (user) {
      form.reset({
        username: user.username,
        group: user.group,
        email: user.email,
        password: "***********"
      })
    }
  }, [user, form])

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



  const debounceTimerRef = useRef(null)

  const onSubmit = ({ password, username, group }) => {
    API.updateUserData({ password, username, group }).then(
      (resp) => {
        if (resp.status === "ok") {
          fetchUser()
          setIsEditable(false)
          showNotificationOuter(resp.detail, "success")
        } else {
          showNotificationOuter(resp.detail, "error")
        }
      }
    )
  }

  const validateGroup = (value) => {
    if (!value?.trim()) return true
  }

  useEffect(() => {
    const timer = debounceTimerRef.current 
    return () => {
      // cleanup при размонтировании
      if (timer) {
        clearTimeout(timer)
      }
    }
  }, [])

  const darkClass = darkTheme ? " dark" : ""

  const usernameInputRef = useRef(null)
  const groupInputRef = useRef(null)
  const passwordInputRef = useRef(null)

  const focusInput = (inputRef) => {
    if (inputRef?.current) {
      const currentInput = inputRef.current
      currentInput.focus()
    } else return
  }

  // ДЛЯ ТОГО ЧТОБЫ ФОКУС СРАБАТЫВАЛ НЕ ТОЛЬКО ПРИ КЛИКЕ НЕПОСРЕДСТВЕННО НА input:
  // сохраняем register поля, чтобы привязать ref и к react-hook-form форме, и к нашим refs
  // в usernameField, groupField, passwordField будет сохранен обьект вида
  // { onChange, onBlur, ref, name, ... }
  const usernameField = register("username", {
    required: false,
    validate: {
      validFormat: async (value) => validateUsername(value),
    },
  })

  const groupField = register("group", {
    required: false,
    validate: {
      validateGroup: (value) => validateGroup(value),
    },
  })

  const passwordField = register("password", {
    required: true,
    // не нужно validate, так как не обновляем пароль, а только проверяем его
  })

  const [isEditable, setIsEditable] = useState(false)

  useEffect(() => {
    if (isEditable) focusInput(usernameInputRef)
    else form.reset()
    // при добавлении form в dependencies логика ломается: при отмене 
    // редактирования, редактируемые поля становится пустыми.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isEditable])

  const handleImmutableFieldClick = (message) => {
    if (!isEditable) return
    showNotificationOuter(message, "error")
  }

  // если isEditable был false (т.е. нажали на кнопку редактировать),
  // то скроллим вниз на кнопку сохранить (для десктопа), а затем меняем его на true
  const saveButtonRef = useRef(null)

  const handleToggleEditing = () => {
    setIsEditable((prev) => {
      if (!prev) {
        passwordInputRef.current.value = ""
        setTimeout(() => {
          // только для десктопа, чтобы скролл не сработал на мобилке. на мобилке только фокус на поле ввода.
          if (width > 1100)
            saveButtonRef.current?.scrollIntoView({ behavior: "smooth" })
        }, 100)
      }
      return !prev
    })
  }

  const navigate = useNavigate()
  const location = useLocation()
  const path = location.pathname.split("/").pop()

  const handleLogout = () => {
    if (path === "profile") {
      navigate("/sign-in")
    }
    API.logout().then((resp) => {
      showNotificationOuter(resp.detail, "error")
      fetchUser()
    })
  }

  if (!user) {
    return (
      <div className="profile">
        <p>пожалуйста, авторизуйтесь. перенаправляю на страницу входа...</p>
      </div>
    )
  }

  return (
    <div className={`profile${darkClass} ${isEditable ? "editing" : ""}`}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="profile__header">
          <div className="profile__header__text">профиль</div>
          <div
            className="profile__header__pencil"
            onClick={handleToggleEditing}
          >
            <img
              className="profile__header__pencil__icon"
              src={
                darkTheme
                  ? isEditable
                    ? pencilIconActiveDark
                    : pencilIconDark
                  : isEditable
                  ? pencilIconActive
                  : pencilIcon
              }
              title="редактировать профиль"
            />
          </div>
        </div>
        <div className="profile__inputs">
          <div className="username-block">
            <label htmlFor="username">имя</label>
            <div
              className={`input-div${darkClass}`}
              onClick={() => focusInput(usernameInputRef)}
            >
              <input
                {...usernameField}
                ref={(el) => {
                  usernameField.ref(el)
                  usernameInputRef.current = el
                }}
                className={`input${darkClass}`}
                type="text"
                id="username"
                readOnly={!isEditable}
              />
              <p className="profile__error">{errors.username?.message}</p>
            </div>
          </div>

          <div className="group-block">
            <label htmlFor="group">группа</label>
            <div
              className={`input-div${darkClass}`}
              onClick={() => focusInput(groupInputRef)}
            >
              <input
                {...groupField}
                ref={(el) => {
                  groupField.ref(el)
                  groupInputRef.current = el
                }}
                className={`input${darkClass}`}
                type="text"
                id="group"
                placeholder="не указана"
                readOnly={!isEditable}
              />
              <p className="profile__error">{errors.group?.message}</p>
            </div>
          </div>

          <div
            className="role-block"
            onClick={() =>
              handleImmutableFieldClick("самому себе роль изменять нельзя :(")
            }
          >
            <label htmlFor="role">роль</label>
            <div className={`input-div${darkClass} immutable-field`}>
              {displayRole.toLowerCase() === "администратор" ? (
                <p>{`${displayRole} (${moderatedGroups})`}</p>
              ) : (
                <p>{displayRole}</p>
              )}
            </div>
          </div>

          <div
            className="email-block"
            onClick={() =>
              handleImmutableFieldClick("электронную почту изменять нельзя :(")
            }
          >
            <label htmlFor="role">эл. почта</label>
            <div className={`input-div${darkClass} immutable-field`}>
              <p>{user?.email}</p>
            </div>
          </div>

          <div className="pwd-block">
            <label htmlFor="password">пароль</label>
            <div
              className={`input-div${darkClass} pwd-input`}
              onClick={() => focusInput(passwordInputRef)}
            >
              <input
                {...passwordField}
                ref={(el) => {
                  passwordField.ref(el)
                  passwordInputRef.current = el
                }}
                className={`input${darkClass}`}
                type="password"
                id="password"
                placeholder="для применения правок..."
                readOnly={!isEditable}
              />
              <p className="profile__error">{errors.password?.message}</p>
            </div>
            {isEditable ? (
              <div className="profile__submit">
                <button
                  className={`profile__submit__cancel__btn${darkClass}`}
                  onClick={handleToggleEditing}
                >
                  отмена
                </button>
                <button
                  className={`profile__submit__save__btn${darkClass}`}
                  type="submit"
                  ref={saveButtonRef}
                >
                  сохранить
                </button>
              </div>
            ) : (
              <div className="profile__submit">
                <div className="profile__submit__logout-wrap">
                  <button
                    type="button"
                    className={`profile__submit__logout__btn${darkClass}`}
                    onClick={handleLogout}
                  >
                    выйти из аккаунта
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </form>
    </div>
  )
}

export default Profile
