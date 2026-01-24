import chel from '../../images/tip/chel.svg'
import chelDark from '../../images/tip/chel-dark.svg'
import tipBg from '../../images/tip/tip-bg.png'
import tipBgNoArrow from '../../images/tip/tip-bg-no-arrow.png'
import tipBgDark from '../../images/tip/tip-bg-dark.png'
import tipBgDarkNoArrow from '../../images/tip/tip-bg-dark-no-arrow.png'
import { useThemeStore } from '../../store/themeStore'
import { useWindowSize } from '../../hooks/useWindowSize'

const Tip = ({active}) => {
  const darkTheme = useThemeStore(state => state.darkTheme)
  const {width} = useWindowSize()
  const noArrow = width < 1101

  return (
  <div 
  className={'tip' + (active? " active" : '') + (darkTheme? ' dark' : '')}
  style={{
    backgroundImage: darkTheme
    ? `url(${noArrow? tipBgDarkNoArrow : tipBgDark})` 
    :`url(${noArrow? tipBgNoArrow : tipBg})`}}>

    <div className="tip__inner">
      <img 
        src={darkTheme? chelDark : chel} 
        alt="Tip" 
      />
      <div className={`tip__text`}>
        <p>выберите вашу группу и неделю, на которую</p>
        <p>хотите посмотреть расписание</p>
      </div>
    </div>
  </div>
  )
}

export default Tip