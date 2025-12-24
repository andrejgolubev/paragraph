import tip from '../images/chel.svg'

const Tip = ({active}) => {
  
  return (<div className={'tip ' + (active && "active")}>
    <div className="tip__inner">
      <img 
      src={tip} 
      alt="Tip" />
      <div className="tip_text">
        <p>выберите вашу группу и неделю, на которую</p>
        <p>хотите посмотреть расписание :)</p>
      </div>
    </div>
  </div>)
}

export default Tip