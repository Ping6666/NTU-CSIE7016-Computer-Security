from os import environ
from fastapi import FastAPI, Request, Body, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from fastapi.templating import Jinja2Templates
import uvicorn
import requests

app = FastAPI()
BANK_API_BASE = environ.get('BANK_API_BASE', 'http://localhost:8080')
with open('/machine-token') as f:
    MACHINE_TOKEN = f.read()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        'BANK_API_BASE': BANK_API_BASE
    })


@app.post("/api/start_game")
async def start_game(user_token: Annotated[str, Body()], bet: Annotated[int, Body()]):
    r = requests.post(BANK_API_BASE + '/api/game/create', json={
        'hashed_user_token': user_token,
        'machine_token': MACHINE_TOKEN,
        'bet': bet
    })
    if r.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=r.status_code, detail=r.json()['detail'])
    return {"game_id": r.json()['uuid']}


if __name__ == "__main__":
    uvicorn.run(app)
