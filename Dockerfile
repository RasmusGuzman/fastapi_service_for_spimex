FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Кладём pyproject.toml и poetry.lock первым делом, чтобы кэшировались слои Docker
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и собираем зависимости
RUN pip install poetry==1.5.* && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Копируем остальной код проекта
COPY . .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]