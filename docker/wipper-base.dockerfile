FROM python:3.9.6-slim
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y && \ 
    apt-get update -y && \
    apt-get install build-essential cmake pkg-config -y && \
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*
RUN pip install dlib==19.9.0