from requester import Response, Requester, ResponseFailed, ResponseSuccess
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
    MODE_STATS = "fastbuilder/{mode}/stats"
    MODE_PLAYER_STATS = "fastbuilder/{mode}/stats/{player}"
    STATS = "fastbuilder/stats"
    PLAYER_STATS = "fastbuilder/stats/{player}"

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


    def _mode_stats(self, mode: Mode) -> Response:
        return self.consume(Endpoints.MODE_STATS, mode=mode.value)


    def _mode_player_stats(self, mode: Mode, player_name: str = "", player_uuid: str = "") -> Response:
        return self.consume(Endpoints.MODE_PLAYER_STATS, mode=mode.value, player=player_uuid or player_name)

    def mode_player_stats(self, mode: Mode, player_name: str = "", player_uuid: str = "") -> BuilderPlayer | None:
        response: Response = self._mode_player_stats(mode, player_name, player_uuid)
        if isinstance(response, ResponseFailed):
            return None
        return BuilderPlayer(response.data)

    def _stats(self) -> Response:
        return self.consume(Endpoints.STATS)

    def _player_stats(self, player_name: str = "", player_uuid: str = "") -> Response:
        return self.consume(Endpoints.PLAYER_STATS, player=player_uuid or player_name)
