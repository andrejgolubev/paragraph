# paragraph
Запуск сервиса и фронтенда -> см. `Makefile`.

# Установка Python-зависимостей
```shell
poetry install
```

# Локальный стек (легкие лимиты)
"-p paragraph" создаёт все ресурсы с префиксом `paragraph_`.
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

# Продакшен-профиль (тяжёлые лимиты)
Тот же стек, но с `docker-compose.prod.yaml`, добавляющим увеличенные лимиты:
```shell
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml -p paragraph up -d
```

# Admin scripts
Для команд управления аккаунтами через `/admin/*` (они уже прикрыты `API-Key`) можно просто запускать curl на сервере:

```bash
./scripts/make-admin.sh user@example.com "543,5413" "$ADMIN_API_KEY" "https://paragraph.example.com"
./scripts/delete-user.sh user@example.com "$ADMIN_API_KEY" "https://paragraph.example.com"
```


# Обновление групп и дат
этот процеесс поднимает `chromedriver`/`Google Chrome for testing` => он должен запускаться в изолированном процессе (по SSH или cron).

1. Установите браузер/драйвер на сервере (Ubuntu):
   ```shell
   sudo apt update
   sudo apt install -y chromium-browser chromium-chromedriver
   ```
2. Запустите обновление через Poetry:
   ```shell
   poetry run python -m backend.api.scripts.reload_db
   ```
   Добавьте `--refresh`, если хотите очистить базу перед загрузкой.
3. Шорткат: `make reload-db`.

Можно поставить cron или systemd timer, чтобы запускать `poetry run python -m backend.api.scripts.reload_db` регулярно 









