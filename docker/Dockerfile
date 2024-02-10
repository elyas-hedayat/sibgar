FROM python:3.11

COPY ./requirements /requirements

RUN pip install --upgrade pip && pip install -r /requirements/base.txt

COPY . /app

WORKDIR /app

EXPOSE 8000