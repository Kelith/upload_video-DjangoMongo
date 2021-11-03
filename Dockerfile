FROM python:bullseye

ENV PYTHONUNBUFFERED 1
RUN mkdir /django_mongodb_docker
WORKDIR /django_mongodb_docker
COPY . /django_mongodb_docker/
RUN pip install --upgrade pip
RUN apt-get update
RUN pip install -r requirements.txt
RUN pip install ffmpeg-python
RUN apt-get install ffmpeg libsm6 libxext6  -y