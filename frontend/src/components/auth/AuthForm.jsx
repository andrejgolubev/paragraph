import React from 'react'

import user_icon from '../../images/auth/person.png'
import password_icon from '../../images/auth/password.png'
import email_icon from '../../images/auth/email.png'


export const AuthForm = ({type}) => {
  // будет переменная userAuthorized с СОСТОЯНИЕМ от которой будет зависеть type 
  // так что такя реализация с let допустима 
  let authType = '' 
  let authTitle = ''

  if (type === 'sign-up') {
    authType = 'Зарегестироваться' 
    authTitle = 'Регистрация'
  } else if (type === 'sign-in') {
    authType = 'Войти' 
    authTitle = 'Вход'
  }
  

  return (
    <div className='container'>
      <div className="container__header">
        <div className="text">{authTitle}</div>
        <div className="underline"></div>
      </div>
      <div className="container__inputs">
        {type === 'sign-up' && (<div className="input">
          <img src={user_icon} alt="user icon" />
          <input type="text" placeholder='Имя'/>
        </div>) }
        <div className="input">
          <img src={email_icon} alt="email icon" />
          <input type="email" placeholder='Электронная почта'/>
        </div>
        <div className="input">
          <img src={password_icon} alt="password icon" />
          <input type="password" placeholder='Пароль' />
        </div>
      </div>
      
      {type === 'sign-in' &&
      (<div className="forgot-password">Забыли пароль?<span> Нажмите сюда</span></div>)}
      <div className="container__submit">
        <div className="container__submit__btn">
          {authType}
        </div>
      </div>
    </div>
  )
}


