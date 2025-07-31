from typing import List

from fastapi import FastAPI, requests
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse, HTMLResponse
from fastapi import Header
from fastapi import Response

app = FastAPI()

@app.get("/ping", status_code=status.HTTP_200_OK)
def read_hello():
    return {"Pong"}


@app.get("/home", status_code=status.HTTP_200_OK)
def welcome_home():
    return HTMLResponse (
        """
            <div>
                <h1>Welcome home !</>
            </div>
        """
    )
class WelcomeRequest(BaseModel):
    name: str

@app.post("/welcome")
def welcome_user(data: WelcomeRequest):
    return {"message": f"Welcome {data.name}"}


class Player (BaseModel):
    Number: int
    Name: str

players_db: List[Player] = []

@app.post("/players", status_code=status.HTTP_201_CREATED)
def add_players (players: List[Player]):
    players_db.extend(players)
    return players_db


@app.get("/players", status_code=status.HTTP_200_OK)
def read_players ():
    return players_db

@app.put("/players", status_code=status.HTTP_200_OK)
def put_players (new_player: Player):
    for i, existing_player in enumerate(players_db):
        if existing_player.Number == new_player.Number:
            if existing_player != new_player:
                players_db[i] = new_player
                return {"message": "Joueur mis à jour", "player": new_player}
            else:
                return {"message": "Aucune modification, joueur identique", "player": new_player}

    players_db.append(new_player)
    return {"message": "Nouveau joueur ajouté", "player": new_player}


@app.put("/top-secret")
def secret_key_verification (authorization: str = Header(...)):
    if (authorization != "my-secret-key"):
        return Response (
            status_code=403,
            media_type="text/plain"
        )
    else:
        return {"message": "Accès autorisé au chemin top-secret"}

@app.get("/verify-code")
def read_secret_code (secret_code: int):
    if(len(str(secret_code)) != 4):
        return JSONResponse (
            status_code=403,
            media_type="text/plain",
            content={"error": f"Il faut un code à 4 chiffres"}
        )
    return {"message": f"Code validé"}