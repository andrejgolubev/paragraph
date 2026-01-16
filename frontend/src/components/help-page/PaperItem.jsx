

export const PaperItem = ({header, content}) => {
  return (
    <div className="paper__content__item">
      <div className="paper__content__item__header">
        <p>{header}</p>
      </div>
      <div className="paper__content__item__content">
        {content.map((text) => <p>{text}</p>)}
      </div>
    </div>
  )
}