import { useContext } from 'react'
import { Context } from '../context/Provider'

import chel from '../images/tip/chel.svg'
import chelDark from '../images/tip/chel-dark.svg'
import tipBg from '../images/tip/tip-bg.png'
import tipBgDark from '../images/tip/tip-bg-dark.png'

const Tip = ({active}) => {
  const {darkTheme} = useContext(Context)

  return (
  <div 
  className={'tip' + (active? " active" : '') + (darkTheme? ' dark' : '')}
  style={{backgroundImage: darkTheme? `url(${tipBgDark})` :`url(${tipBg})`}}>
    <div className="tip__inner">
      <img 
        src={darkTheme? chelDark : chel} 
        alt="Tip" 
      />
      <div className={`tip__text`}>
        <p>выберите вашу группу и неделю, на которую</p>
        <p>хотите посмотреть расписание :)</p>
      </div>
    </div>
  </div>
  )
}

export default Tip