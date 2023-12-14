# Wipper API
API for the Wipper mobile app.

## Local Usage:
Inside the wipper-api directory run the following commands:
- `pip install -r requirements.txt`
- `python .\main.py`

## Using Docker:
Run the following commands:
- `docker build -t wipper-base:0.0.1  -f docker/wipper-base.dockerfile .`
- `docker build -t wipper-api:0.0.1 .`
- `docker run -p 8000:8000 -d wipper-api:0.0.1`

Access the documentation on `http://localhost:8000\docs`