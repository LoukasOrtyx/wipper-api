FROM wipper-base:0.0.1
WORKDIR /app
COPY . .

# RUN pip install torch==1.9.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html && \
# 	pip install torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install -r requirements.txt
EXPOSE 8000
ENV PYTHONPATH "${PYTHONPATH}."
ENTRYPOINT [ "python3", "main.py" ]