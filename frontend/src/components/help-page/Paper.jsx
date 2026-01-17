import { useThemeStore } from "../../store/themeStore"
import { PaperItem } from "./PaperItem"

export const Paper = ({ type }) => {
  const darkTheme = useThemeStore((state) => state.darkTheme)

  const paperTitles = {
    privacy: "Политика конфиденциальности",
    terms: "Пользовательское соглашение",
    pd: "Согласие на обработку персональных данных",
  }

  const paperLastUpdate = {
    privacy: '17.01.2026',
    terms: '18.01.2026',
    pd: '19.01.2026',
  }

  const privacyIntro = `В Политике конфиденциальности (далее — Политика) указан перечень персональных 
  данных (далее — Данные), которые могут быть запрошены у пользователей (далее — Пользователь) 
  на веб-сайте, расположенном по адресу https://paragraph-schedule.ru (далее — Сайт), а также способы обработки таких данных.
  Политика применяется также к информации, которую Голубев Андрей Александрович (далее — Оператор) 
  получил в результате эксплуатации Сайта Пользователем.`

  const paperContent = {
    privacy: {
      headers: [
        `1. Dfjsdiofjsoi Ooij privacy`,
        `2. Jfghskofhj Jdjg privacy`,
        `3. Doksdopj Dpojsp privacy`,
      ],
      content: [
        [
          `1.1. privacy ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
          `1.2. privacy ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
        ],
        [
          `2.1. privacy ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
          `2.2. privacy ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
        ],
        [
          `3.1. privacy ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
          `3.2. privacy ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
          `3.3. privacy ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
        ]
      ]
    },
    terms: {
      headers: [
        `1. Dfjsdiofjsoi Ooij terms`,
        `2. Jfghskofhj Jdjg terms`,
        `3. Doksdopj Dpojsp terms`,
      ],
      content: [
        [
          `1.1. terms ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
          `1.2. terms ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
        ],
        [
          `2.1. terms ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
          `2.2. terms ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
        ],
        [
          `3.1. terms ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
          `3.2. terms ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
          `3.3. terms ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
        ]
      ]
    },
    pd: {
      headers: [
        `1. Dfjsdiofjsoi Ooij pd`,
        `2. Jfghskofhj Jdjg pd`,
        `3. Doksdopj Dpojsp pd`,
      ],
      content: [
        [
          `1.1. pd ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
          `1.2. pd ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
        ],
        [
          `2.1. pd ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
          `2.2. pd ipsum dolor sit amet consectetur adipisicing elit. Omnis dolorem
              distinctio dicta libero, error vero in repellendus excepturi eos,
              quaerat aliquid quisquam sit! Nemo, repudiandae?`,
        ],
      ]
    }
  }


  return (
    <div className={`paper ${darkTheme ? "dark" : ""}`}>
      <div className="paper__header">
        {paperTitles[type]}
      </div>
      <div className="paper__last-update">
        {`редакция от ${paperLastUpdate[type]}`}
      </div>
      <div className="paper__content">
        {type === 'privacy' && 
        <div className="paper__content__intro">
          {privacyIntro}
        </div>
        }
        {paperContent[type].headers.map((header, index) => (
          <PaperItem
            header={header}
            content={paperContent[type].content[index] ?? []}
            key={header}
          />
        ))}
      </div>
    </div>
  )
}
