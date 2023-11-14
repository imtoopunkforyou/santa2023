import enum
from typing import Tuple


@enum.unique
class CommandsEnum(enum.Enum):
    """
    Bot commands.

    Attributes
    ----------
    HELP: str
        ...
    START: str
        ...
    LIST: str
        ...
    ME: str
        ...
    WISH: str
        ...
    DB: str
        ...
    """

    HELP = 'help'
    START = 'start'
    LIST = 'list'
    ME = 'me'
    WISH = 'wish'
    DB = 'db'
    ADD_PLAYERS = 'add_players'
    RESTORE_PLAYER = 'restore_player'

    @classmethod
    def get_names(cls) -> Tuple[str]:
        return tuple(i.name for i in cls)

    @classmethod
    def get_values(cls) -> Tuple[str]:
        return tuple(i.value for i in cls)
