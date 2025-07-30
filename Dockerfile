FROM python:3.10

WORKDIR /app

# Копіюємо всі файли відразу, включно з README.md
COPY . /app

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
