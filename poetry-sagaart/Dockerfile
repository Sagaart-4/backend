FROM python:3.11

RUN apt-get update && \
    pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY ./pyproject.toml ./

RUN poetry install

COPY ./ ./

CMD ["gunicorn", "sagaart.wsgi:application", "--access-logfile '-'", "--error-logfile '-'", "--bind", "0:8000" ]
