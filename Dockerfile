FROM python:3.11.0-bullseye

ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code

COPY ./app/ /code/

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root
