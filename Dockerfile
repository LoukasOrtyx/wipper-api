FROM wipper-base-inpainting:0.0.1
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
ENV PYTHONPATH "${PYTHONPATH}."
ENTRYPOINT [ "python3", "main.py" ]