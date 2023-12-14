FROM wipper-base:0.0.1
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT [ "python", "main.py" ]