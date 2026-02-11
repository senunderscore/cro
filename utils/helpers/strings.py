import json
import random
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
STRINGS_PATH = Path("data") / "strings.json"


def load_strings() -> dict:
    try:
        with open(STRINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.debug("strings.json not found; returning empty dict")
        return {}
    except json.JSONDecodeError:
        logger.exception("Failed to parse strings.json")
        return {}


def get_list(key: str, default: list) -> list:
    strings = load_strings()
    value = strings.get(key)
    if isinstance(value, list) and value:
        return value
    return default


def get_random(key: str, default: list) -> str:
    choices = get_list(key, default)
    try:
        return random.choice(choices)
    except Exception:
        return default[0] if default else ""
