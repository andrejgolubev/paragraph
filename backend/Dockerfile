FROM python:3.12.6-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/

WORKDIR /backend

RUN apt-get update 

# Python dependencies 
RUN pip install --upgrade pip poetry 

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false 


COPY . .


# Unzip Chromedriver (Unzipping Chrome for testing in ./prestart.sh)
RUN unzip /backend/chromedriver-linux64.zip -d /backend/ \
&& rm /backend/chromedriver-linux64.zip


# RUN poetry install --only main --no-interaction --no-ansi
# Хорошо для CI/CD, но не для первоначального поднятия контейнера.
# Используем дефолтную установку зависимостей: 
RUN poetry install --no-root
    
    
RUN chmod +x prestart.sh
RUN chmod +x start.sh

ENTRYPOINT ["./prestart.sh"]

CMD ["./start.sh"]
