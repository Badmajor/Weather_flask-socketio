FROM python:3.12-alpine3.19 AS requirements-stage

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk update && \
    python -m pip install --upgrade pip --no-cache-dir && \
    pip install poetry

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry export -f requirements.txt --output requirements.txt \
    --without-hashes

FROM python:3.12-alpine3.19

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --from=requirements-stage /requirements.txt ./requirements.txt

RUN apk update && \
    python -m pip install --upgrade pip --no-cache-dir && \
    pip install -r requirements.txt --no-cache-dir

RUN pip install gunicorn==22.0.0

COPY . .


CMD ["gunicorn", "-k", "eventlet", "-b", "0.0.0.0:8000", "app_tools:create_app()"]