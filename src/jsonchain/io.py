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
