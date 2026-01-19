# paragraph 

# установка зависимостей 
poetry install

# Локальный стек 
"-p paragraph" - создает все ресурсы с префиксом "paragraph_"
- сборка и поднятие:
  ```shell
  docker compose -p paragraph up -d
  ```
- остановка:
  ```shell
  docker compose -p paragraph down
  ```
- удаление томов:
  ```shell
  docker compose -p paragraph down --volumes
  ```
- статус:
  ```shell
  docker compose -p paragraph ps
  ```


# Продакшен-профиль 
- Тот же стек, но с «продакшеновыми» лимитами, перечисленными в `docker-compose.prod.yaml`:
```shell
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml -p paragraph up -d
```









