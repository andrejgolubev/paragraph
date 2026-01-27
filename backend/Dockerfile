FROM python:3.12.6-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /backend 

RUN apt-get update


# Python dependencies 
RUN pip install --upgrade pip poetry 

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false 

COPY . .

# RUN poetry install --only main --no-interaction --no-ansi
# Хорошо для CI/CD, но не для первоначального поднятия контейнера.
# Используем дефолтную установку зависимостей: 
RUN poetry install --no-root
    
    
# Chrome for testing install
RUN chmod +x scripts/prestart.sh
RUN chmod +x scripts/start.sh

ENTRYPOINT ["./scripts/prestart.sh"]

CMD ["./scripts/start.sh"]
