import enum
from typing import Tuple


@enum.unique
class CommandsEnum(enum.Enum):
    """
    Bot commands.

    Attributes
    ----------
    BASE_HELP: str
        For show all commands.
    BASE_START: str
        For first user telegram message.
    BASE_LIST: str
        For show all players. (registration)

    INDIVIDUAL_ME: str
        For show individual player info.
    INDIVIDUAL_WISH: str
        To add individual player wish.

    ADMIN_DB: str
        For show all info about players. (admin command).
    ADMIN_ADD_PLAYERS: str
        To add two players.
    ADMIN_RESTORE_PLAYER: str
        To restore player registration.
    """

    BASE_HELP = 'help'
    BASE_START = 'start'
    BASE_LIST = 'list'

    PERSONAL_ME = 'me'
    PERSONAL_WISH = 'wish'

    ADMIN_DB = 'db'
    ADMIN_ADD_PLAYERS = 'add_players'
    ADMIN_RESTORE_PLAYER = 'restore_player'

    @classmethod
    def get_names(cls) -> Tuple[str]:
        """All attribute names in class."""
        return tuple(i.name for i in cls)

    @classmethod
    def get_values(cls) -> Tuple[str]:
        """All values of attributes in class."""
        return tuple(i.value for i in cls)

    @classmethod
    def get_user_commands(cls) -> Tuple[str]:
        """All values of attributes like telegram commands."""
        all_commands = tuple(i for i in cls)
        user_commands = []
        for command in all_commands:
            if 'ADMIN_' not in command.name:
                user_commands.append('/' + command.value)
        return tuple(user_commands)
