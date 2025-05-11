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
    def _modes(self) -> Response:
        return self.ask(Endpoints.MODES)

    @property
    def modes(self) -> list[Mode]:
        return [Mode[name] for name in self._modes.data.get("modes", [])]

    def _top(self, mode: Mode) -> Response:
        return self.consume(Endpoints.MODE_TOP, mode=mode.value)

    def top(self, mode: Mode) -> list[BuilderPlayer]:
        response: Response = self._top(mode)
        if isinstance(response, ResponseSuccess):
            return [BuilderPlayer(player_data) for player_data in response.data]
        return []
