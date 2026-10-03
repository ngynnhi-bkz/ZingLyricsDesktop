from fastapi import FastAPI, Body, Query
from fastapi.middleware.cors import CORSMiddleware

from models import PlayerState
from player import player
import lyrics


app = FastAPI(
    title="Zing Lyrics Desktop",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


@app.get("/")
def root():

    return {
        "status": "running"
    }


@app.get("/player")
def get_player():

    return player.get()


@app.post("/player/update")
def update_player(
    state: PlayerState
):

    player.update(state)

    return {
        "success": True
    }


@app.post("/lyrics/update")
def update_lyrics(
    data: dict = Body(...)
):

    lyrics.update(data)

    return {
        "success": True
    }


@app.get("/lyrics")
def get_lyrics():

    return lyrics.get()


@app.get("/current_lyrics")
def current_lyrics(
    time_ms: int | None = Query(
        default=None
    )
):

    return lyrics.get_current(
        time_ms
    )