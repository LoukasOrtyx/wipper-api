FROM python:3.9.6-slim
WORKDIR /app
COPY . .
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update -y && \
    apt-get install build-essential cmake pkg-config -y
RUN pip install dlib==19.9.0 && pip install face-recognition 
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT [ "python", "main.py" ]