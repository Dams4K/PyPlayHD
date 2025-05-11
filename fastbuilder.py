from requester import Response, Requester, ResponseSuccess
from enum import StrEnum, auto
from player import BuilderPlayer

class Mode(StrEnum):
    NORMAL = auto()
    SHORT = auto()
    EXTRASHORT = auto()
    LONG = auto()
    INCLINED = auto()
    INCLINEDSHORT = auto()
    ONESTACK = auto()
    INFINITE = auto()

class Endpoints:
    MODES = "fastbuilder/modes"
    MODE_TOP = "fastbuilder/{mode}/top"

class FastBuilder(Requester):
    @property
    def modes(self) -> list[Mode]:
        response: Response = self.ask(Endpoints.MODES)
        return [Mode[name] for name in response.data.get("modes", [])]

    def top(self, mode: Mode) -> list[BuilderPlayer]:
        response: Response = self.consume(Endpoints.MODE_TOP, mode=mode.value)
        if isinstance(response, ResponseSuccess):
            return [BuilderPlayer(player_data) for player_data in response.data]
        return []
