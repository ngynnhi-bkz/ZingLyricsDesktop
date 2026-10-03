from models import PlayerState


class Player:

    def __init__(self):
        self.state = PlayerState()

    def update(self, state: PlayerState):
        self.state = state

    def get(self):
        return self.state.model_dump()


player = Player()