import HomeworkModal from "./HomeworkModal"

const MainContent = () => {
  return (
    <div className="main-content">
      <div className="options">
        <div className="group">
          <div className="custom-select">
            <div className="search-block">
              <div className="search-block__body">
                <div className="search-block__wrap-input">
                  <input
                    type="text"
                    id="search-input"
                    placeholder="номер группы"
                    className="search-block__input"
                  />
                </div>
                <ul className="search-block__products" id="products" />
              </div>
            </div>
          </div>
        </div>
        <div className="week">
          <div className="custom-select">
            <div className="select-block">
              <div className="select-block__body">
                <div className="select-block__wrap-input">
                  <input
                    readOnly
                    type="text"
                    id="select-input"
                    placeholder="дата/неделя"
                    className="search-block__input"
                  />
                </div>
                <ul className="select-block__products" id="dates" />
              </div>
            </div>
          </div>
        </div>
        <div className="corpuses">
          <p>C - Центральный корпус⠀⠀⠀⠀B - Бизнес-инкубатор</p>
          <p>L - Лабораторный корпус ⠀⠀⠀F - Первый корпус</p>
        </div>
      </div>
      <div className="tip">
        <div className="tip__inner">
          <img src="../static/static/chel.svg" alt="Tip" />
          <div className="tip_text">
            <p>выберите вашу группу и неделю, на которую</p>
            <p>хотите посмотреть расписание :)</p>
          </div>
        </div>
      </div>
      
      <HomeworkModal />
      {/* notification outer*/}
      {/* ... */}

    </div>
  )
}

export default MainContent
