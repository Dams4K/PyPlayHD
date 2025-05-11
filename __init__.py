from fastbuilder import FastBuilder

class Client:
    def __init__(self, token: str):
        self.token = token

        self.fastbuilder = FastBuilder(token)
