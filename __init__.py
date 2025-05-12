from .fastbuilder import *
from .player import *

class Client:
    def __init__(self, token: str):
        self.token = token

        self.fastbuilder = FastBuilder(token)
