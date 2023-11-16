import conf


def is_admin(telegram_id: int) -> bool:
    """
    Cheque whether the user is an admin.

    Args:
        telegram_id (int): user telegram id.
    Returns:
        bool: result of checking. True if user is admin.
    """
    if telegram_id in conf.BOT_ADMINS:
        return True

    return False
