# Как устанавливать на Ubuntu "Chrome browser for testing"

- 1. Скачиваем официальную сборку Chrome 144.0.7559.96 для Linux с 
https://googlechromelabs.github.io/chrome-for-testing/
```bash
curl -L -o chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/144.0.7559.96/linux64/chrome-linux64.zip
``` 
(при работе с контейнером - заранее переходим по ссылке и качаем. Желательно добавить 
в том - файл весит довольно много)


- 2. Устанавливаем зависимости системного уровня, необходимые для архивированных бинарников linux64. Команда взята отсюда: 
https://github.com/GoogleChromeLabs/chrome-for-testing 
```bash 
unzip chrome-linux64.zip;
apt-get update;
while read pkg; do
  apt-get satisfy -y --no-install-recommends "${pkg}";
done < chrome-linux64/deb.deps; 
```

При работе с контейнером лучше заранее скачать Chrome, скопировать в рабочую директорию 
контейнера при помощи Dockerfile COPY, а затем выполнять распаковку командой: 
```bash
if [ -f /backend/chrome-linux64.zip ] && [ ! -d /backend/chrome-linux64 ]; then
  unzip /backend/chrome-linux64.zip -d /backend
  apt-get update
  while read pkg; do
    apt-get satisfy -y --no-install-recommends "${pkg}"
  done < /backend/chrome-linux64/deb.deps
  echo "Chrome Browser for testing downloaded!"
else
  echo "Chrome Browser for testing did not download"
fi
```

- 3. Скачиваем Chromedriver 144.0.7559.96 (версия для примера, версии должны совпадать
с Chrome): https://storage.googleapis.com/chrome-for-testing-public/144.0.7559.96/linux64/chromedriver-linux64.zip
```bash
curl -L -o chromedriver-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/144.0.7559.96/linux64/chrome-linux64.zip
``` 
(при работе с контейнером - переходим по ссылке и качаем. Затем добавляем в том при
необходимости - файл легковесный, можно и просто Dockerfile COPY)

- 4. Конфигирируем парсер с selenium по примеру из api/parser/config.py. 
При запуске контейнера backend, Chrome/Chromedriver могут долго качаться/тупить 10-15 секунд и выдавать ошибку, надо просто подождать. В логах все будет

- 5. Готово! Можно запускать `make reload-db` (см. `./Makefile`)


# Установка Python-зависимостей - "CI/CD профиль" 
- 1. Вместо `poetry install` запускаем: 
```Dockerfile
RUN poetry install --only main --no-interaction --no-ansi
```