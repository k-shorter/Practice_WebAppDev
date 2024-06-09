import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import events, participants, restaurants, reservations

# 現在の環境を取得
env = os.getenv('ENV', 'development') # デフォルトを開発環境とする
# 環境に応じて.envファイルを読み込む
if env == 'development':
    dotenv_path = '.env.dev'
else:
    dotenv_path = '.env.prod'
load_dotenv(dotenv_path)

REACT_URL = os.getenv('REACT_URL')

app = FastAPI()
# 静的ファイルのディレクトリを指定
app.mount("/images", StaticFiles(directory="images"), name="images")

origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
async def hello():
    return {"message": "Hello World!"}

app.include_router(events.router)
app.include_router(participants.router)
app.include_router(restaurants.router)
app.include_router(reservations.router)