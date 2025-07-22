from copy import copy
from typing import Hashable

def compare_tree_values(
    tree_a: dict | list,
    tree_b: dict | list,
    levels_a: list[Hashable | None],
    levels_b: list[Hashable | None],
    leaves_a: list[Hashable | None],
    leaves_b: list[Hashable | None],
    compare_func: str | callable,
    name_key: Hashable,
    *args,
    **kwargs,
) -> dict:
    """
    Returns a dictionary tree keyed according to 
    'tree_a': the first tree to compare
    'tree_b': the second tree to compare
    'levels_a': The levels to iterate through in order to access the leaf keys in
        'leaves_a'. If a level is listed is None, then all keys at that level will
        be iterated over.
    'levels_b': The levels to iterate through in order to access the leaf keys in
        'leaves_b'. If a level is listed is None, then all keys at that level will
        be iterated over.
    'leaves_a': a list of leaf keys to compare. Must be same length as 'leaves_b'.
    'leaves_b': a list of leaf keys to compare. Must be same length as 'leaves_a'.
    'compare_func': Either one of 
        {'div', 'sub', 'add', 'mult', 'ge', 'le', 'lt', 'gt', 'eq', 'ne'} or a 
        user-supplied callable whos call signature takes the values of the individul
        elements of 'leaves_a' as the first param, the individual elements of 'leaves_b'
        as the second param. Optionally, args and kwargs can be passed and they
        will be passed on to the callable.
    """