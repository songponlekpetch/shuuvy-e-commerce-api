FROM python:3.11.0-buster

ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code

COPY ./app/ /code/

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry update
RUN poetry install --no-root
