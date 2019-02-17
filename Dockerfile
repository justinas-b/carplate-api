FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY . /code/
WORKDIR /code
RUN pip install -r requirements.txt
