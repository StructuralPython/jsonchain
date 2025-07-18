"""
A small package to aid in the use of the chaining techniques taught by Structural Python
"""

__version__ = "0.1.0"


import json
import pathlib
from typing import Any, Optional

def load_json(filepath: str | pathlib.Path) -> dict | list:
    """
    Loads the JSON data at 'filepath' into a Python object.
    """
    with open(filepath, 'r') as file:
        return json.load(file)
    

def dump_json(object: list | dict, filepath: str | pathlib.Path, indent=2) -> None:
    """
    Dumps the 'object' (which must be JSON-serializable) into a JSON
    file at 'filepath'.
    """
    with open(filepath, 'w') as file:
        json.dump(object, file, indent=indent)


def extract_keys(
        object: dict[str, Any], 
        key_name: str,
        include_startswith: Optional[str] = None,
        exclude_startswith: Optional[str] = None,
    ) -> list[dict[str, Any]]:
    """
    Returns a list of dicts where each dict has a key of 'key_name'
    and a value of one of the keys of 'object'.

    e.g.
    object = {"key1": value, "key2": value, "key3": value}
    key_name = "label"

    extract_keys(object, key_name) # [{"label": "key1"}, {"label": "key2"}, {"label": "key3"}]

    'include_startswith': If provided, will only include keys that start with this string.
    'exclude_startswith': If provided, will exclude all keys that start with this string.

    If both 'include_startswith' and 'exclude_startswith' are provided, exclude is executed
    first.
    """
    shortlist = []
    for key in object.keys():
        if exclude_startswith is not None and key.startswith(exclude_startswith):
            continue
        else:
            shortlist.append(key)

    acc = []
    for key in shortlist:
        if include_startswith is not None and key.startswith(include_startswith):
            acc.append({key_name: key})
        elif include_startswith is None:
            acc.append({key_name: key})

    return acc