# FROM python:3.11-slim

# WORKDIR /app

#ENV PYTHONDONTWRITEBYTECODE=1 \
   # PYTHONUNBUFFERED=1

#COPY requirements.txt /app/
#RUN pip install --no-cache-dir -r requirements.txt

#COPY . /app/

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Этап 1: Сборка (используем slim вместо alpine)
FROM python:3.11-slim AS builder

WORKDIR /app

# Устанавливаем uv
RUN pip install --no-cache-dir uv

# Настройка путей
ENV UV_PROJECT_ENVIRONMENT=/usr/local

COPY pyproject.toml uv.lock ./

# Установка зависимостей
RUN uv sync --no-install-project --no-dev

# ---------------------------------------------------
# Этап 2: Финальный образ (тот же дистрибутив - slim)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Теперь файлы, скопированные отсюда, будут работать
COPY --from=builder /usr/local /usr/local

COPY . /app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
