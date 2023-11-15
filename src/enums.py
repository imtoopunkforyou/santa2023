import enum
from typing import Tuple


@enum.unique
class CommandsEnum(enum.Enum):
    """
    Bot commands.

    Attributes
    ----------
    HELP: str
        For show all commands.
    START: str
        For first user telegram message.
    LIST: str
        For show all players. (registration)
    ME: str
        For show individual player info.
    WISH: str
        To add individual player wish.
    DB: str
        For show all info about players. (admin command).
    ADD_PLAYERS: str
        To add two players.
    RESTORE_PLAYER: str
        To restore player registration.
    REGEXP_1_100: str
        Regular expression for numbers in 1-100.
    """

    HELP = 'help'
    START = 'start'
    LIST = 'list'
    ME = 'me'
    WISH = 'wish'
    DB = 'db'
    ADD_PLAYERS = 'add_players'
    RESTORE_PLAYER = 'restore_player'
    REGEXP_1_100 = r'^([1-9][0-9]?|100)$'

    @classmethod
    def get_names(cls) -> Tuple[str]:
        """All attribute names in class."""
        return tuple(i.name for i in cls)

    @classmethod
    def get_values(cls) -> Tuple[str]:
        """All values of attributes in class."""
        return tuple(i.value for i in cls)
