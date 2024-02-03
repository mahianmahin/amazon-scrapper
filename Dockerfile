FROM python:3.10

WORKDIR /scrapper

COPY . /scrapper

RUN pip install -r requirements.txt

