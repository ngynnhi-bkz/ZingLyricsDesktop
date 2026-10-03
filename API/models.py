from pydantic import BaseModel


class PlayerState(BaseModel):
    title: str = ""
    url: str = ""
    artist: str = ""
    current_time: float = 0.0
    duration: float = 0.0
    playing: bool = False