# Как устанавливать на Linux "Chrome browser for testing"

- 1. Скачиваем официальную сборку Chrome 144.0.7559.96 для Linux с 
https://googlechromelabs.github.io/chrome-for-testing/
(для docker compose заранее скачиваем и монтируем том)
```bash
curl -L -o chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/144.0.7559.96/linux64/chrome-linux64.zip
``` 

- 2. Устанавливаем зависимости системного уровня, необходимые для архивированных бинарников linux64. Команда взята отсюда: 
https://github.com/GoogleChromeLabs/chrome-for-testing 
```bash 
unzip chrome-linux64.zip;
apt-get update;
while read pkg; do
  apt-get satisfy -y --no-install-recommends "${pkg}";
done < chrome-linux64/deb.deps; 
```

# Установка Python-зависимостей - "CI/CD профиль" 
- 1. Вместо poetry install запускаем: 
```Dockerfile
RUN poetry install --only main --no-interaction --no-ansi
```