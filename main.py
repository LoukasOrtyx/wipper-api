import uvicorn
from fastapi import FastAPI
from routes import recognition
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(recognition.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)