from enum import StrEnum, auto

class PlayerGroup(StrEnum):
    PLAYER = auto()
    PREMIUM = auto()
    VIP = auto()
    MVP = auto()
    YOUTUBER = auto()
    BUILDER = auto()
    HELPER = auto()
    MODERATOR = auto()
    SRMOD = auto()
    DEVELOPER = auto()
    ADMIN = auto()
    OWNER = auto()

class PlayerInfo:
    def __init__(self, uuid: str, name: str, group: PlayerGroup) -> None:
        self.uuid: str = uuid
        self.name: str = name
        self.group: PlayerGroup = group

    @classmethod
    def from_data(cls, data: dict):
        return cls(data["uuid"], data["name"], PlayerGroup[data["group"]])
    
    def __repr__(self):
        attrs = [(attr_name, getattr(self, attr_name)) for attr_name in [attr for attr in self.__dict__ if not attr.startswith("_")]]
        inner = ' '.join("%s=%r" % t for t in attrs)
        return f'<{self.__class__.__name__} {inner}>'


class BuilderStats:
    def __init__(self,
        games: int = 0,
        wins: int = 0,
        blocks: int = 0,
        time_best: int = -1,
        time_total: int = -1,
        confirmed: bool = False,
        speedrun_confirmed: bool = False
    ) -> None:
        self.games = games
        self.wins = wins
        self.blocks = blocks
        self.time_best = time_best
        self.time_total = time_total
        self.confirmed = confirmed
        self.speedrun_confirmed = speedrun_confirmed

    @property
    def average_time(self) -> int:
        return round(self.time_total / self.wins)

    @classmethod
    def from_data(cls, data):
        if data is None:
            return cls()
        return cls(
            data.get("games", 0),
            data.get("wins", 0),
            data.get("blocks", 0),
            data.get("timeBest", -1),
            data.get("timeTotal", -1),
            data.get("confirmed", False),
            data.get("speedrunConfirmed", False)
        )


    def __repr__(self):
        attrs = [(attr_name, getattr(self, attr_name)) for attr_name in [attr for attr in self.__dict__ if not attr.startswith("_")]]
        inner = ' '.join("%s=%r" % t for t in attrs)
        return f'<{self.__class__.__name__} {inner}>'


class BuilderPlayer:
    def __init__(self, data: dict) -> None:
        self.player_info: PlayerInfo = PlayerInfo.from_data(data["playerInfo"])
        self.builder_stats: BuilderStats = BuilderStats.from_data(data["stats"])
    
    def __repr__(self):
        attrs = [(attr_name, getattr(self, attr_name)) for attr_name in [attr for attr in self.__dict__ if not attr.startswith("_")]]
        inner = ' '.join("%s=%r" % t for t in attrs)
        return f'<{self.__class__.__name__} {inner}>'
