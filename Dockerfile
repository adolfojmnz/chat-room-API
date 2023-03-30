FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY Pipfile* /usr/src/app

RUN pip install pipenv && pipenv install && pipenv shell

COPY . /usr/src/app