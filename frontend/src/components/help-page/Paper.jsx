import { useThemeStore } from "../../store/themeStore"
import { PaperItem } from "./PaperItem"

export const Paper = ({ type }) => {
  const darkTheme = useThemeStore((state) => state.darkTheme)
  const paperContent = {
    headers: type === 'privacy' ? [
      `1. Dfjsdiofjsoi Ooij privacy`,
      `2. Jfghskofhj Jdjg privacy`,
      `3. Doksdopj Dpojsp privacy`,
      ] : type === 'terms' ? [
        `1. Dfjsdiofjsoi Ooij terms`,
        `2. Jfghskofhj Jdjg terms`,
        `3. Doksdopj Dpojsp terms`,
      ] : [
        `1. Dfjsdiofjsoi Ooij pd`,
        `2. Jfghskofhj Jdjg pd`,
        `3. Doksdopj Dpojsp pd`,
      ],
    content: type === 'privacy' ? [
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
    ] : type === 'terms' ? [
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
    ] : [
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

  return (
    <div className={`paper ${darkTheme ? "dark" : ""}`}>
      <div className="paper__header">
        {type === "terms"
          ? "Пользовательское соглашение"
          : type === "privacy"
          ? "Политика конфиденциальности"
          : "Согласие на обработку персональных данных"}
      </div>
      <div className="paper__content">
        {paperContent.headers.map((header, index) => (
          <PaperItem
            header={header}
            content={paperContent.content[index] ?? []}
            key={header}
          />
        ))}
      </div>
    </div>
  )
}
