import random
from typing import List, Tuple


def make_pairs(ls: List[int]) -> List[Tuple[int, int]]:
    """
    Divides list into (player_id, santa_id) pairs.

    Args:
        ls (List[int]): List of players ids.
    Raises:
        ValueError: Intended for lists of even length only.
    Returns:
        List[Tuple[int, int]]: List of (player_id, santa_id) pairs.
    """
    if len(ls) % 2 != 0:
        raise ValueError('List must have even number of elements.')

    _ls = ls.copy()
    random.shuffle(_ls)

    pairs = []

    for _ in range(len(_ls)):
        player = _ls[0]
        santa = _ls[-1]
        pairs.append((player, santa))
        _ls.remove(player)
        _ls.append(player)

    return pairs
