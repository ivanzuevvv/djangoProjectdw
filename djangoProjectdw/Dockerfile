# Базовый образ
FROM python:3.9-alpine

# Установка рабочей директории
WORKDIR /djangoProjectdw

# Обновление пакетов и установка зависимостей
RUN apk update && apk add --no-cache gcc musl-dev linux-headers

# Установка зависимостей Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновление pip и установка зависимостей Python
RUN pip install --upgrade pip
COPY requirements.txt /djangoProjectdw/requirements.txt
RUN pip install -r requirements.txt

# Копирование кода приложения
COPY . /djangoProjectdw