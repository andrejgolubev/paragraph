# paragraph
Приветствую в репозитории электронный дневника "параграф"! 
[Дневник](https://paragraph-schedule.ru) - веб-сайт, где живёт "параграф".

Ниже представлено краткое руководство по локальному запуску, если Вам такое надо.

# Локальный запуск 
Запуск бекенда и фронтенда локально -> см. `Makefile` в корне проекта. Там команды 
для запуска backend по https, для этого нужен mkcert: 
https://github.com/FiloSottile/mkcert

Можно запускать и по http, написав свой шорткат, или любым другим способом.

## Установка Backend-зависимостей
```shell
cd backend && poetry install
```

## Миграции в базу данных. БД можно поднять в docker.
```shell 
alembic upgrade head 
```

## Аутентификация
Для работы системы аутентификации понадобится поработать с ключами.
Перейдите в `backend/api/auth/README.md`, там находятся команды для генерации 
ключей. Создайте директорию `backend/api/certs` , перейдите в нее, и там выполните 
эти команды. Создастся пара ключей: приватный и публичный. Готово!

## Установка Frontend-зависимостей 
```shell 
cd frontend && npm install 
```

## Локальный стек 
- сборка и поднятие:
  ```shell
  docker compose up -d
  ```
- остановка:
  ```shell
  docker compose down
  ```
- статус:
  ```shell
  docker compose ps -a
  ```

## Обновление групп и дат
см. `backend/README.md`

## Админские shell-скрипты
Для команд управления аккаунтами через `/admin/*` (прикрыты `API-Key`) можно просто запускать curl на сервере:

```bash
./backend/scripts/make-admin.sh user@example.com 543,5413 "$ADMIN_API_KEY" "https://api.paragraph-schedule.ru"
./backend/scripts/delete-user.sh user@example.com "$ADMIN_API_KEY" "https://api.paragraph-schedule.ru"
```
И так далее, см. backend/scripts для других скриптов. Локально проще использовать
интерактивную документацию /docs или /redoc. 
Изначально у Вас локально она будет включена (см. `backend/core/config.py`), 
но ее можно выключить, прописав `DOCS__ENABLED=false` в .env в корне проекта. 

## Переменные окружения 
Почти все переменные окружения можно выставить, основываясь на docker-compose.yaml
в корне проекта, `backend/core/config.py` и `frontend/vite.config.js`. 
Примечание: 
backend использует переменные окружения из .env в корне, frontend - из .env внутри 
директории frontend









