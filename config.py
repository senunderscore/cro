from pathlib import Path
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

def _first(*names):
    for n in names:
        v = os.getenv(n)
        if v is not None:
            return v
    return None

TOKEN: str = _first('DISCORD_TOKEN', 'TOKEN') or ''

_masters = os.getenv('BOT_MASTERS', '')
BOT_MASTERS: List[str] = [m.strip() for m in _masters.split(',') if m.strip()]

STEAM_API_KEY: str = os.getenv('STEAM_API_KEY', '')
TWITCH_CLIENT_ID: str = os.getenv('TWITCH_CLIENT_ID', '')
TWITCH_CLIENT_SECRET: str = os.getenv('TWITCH_CLIENT_SECRET', '')
YOUTUBE_API_KEY: str = os.getenv('YOUTUBE_API_KEY', '')


def validate(raise_on_missing: bool = True) -> List[str]:
    """Validate required configuration and return a list of issues.

    If `raise_on_missing` is True the function raises RuntimeError when required
    items are missing (useful for startup). otherwise it returns a list of
    human-readable problems (hopefully).
    """
    problems = []
    if not TOKEN:
        problems.append("TOKEN (DISCORD_TOKEN or TOKEN) is not set")

    if raise_on_missing and problems:
        raise RuntimeError("Configuration invalid: " + "; ".join(problems))

    return problems


def create_env_template(path: str = '.env') -> None:
    """Write a `.env` template file to `path`. Does not overwrite existing file."""
    p = Path(path)
    if p.exists():
        return

    content = (
        "# Example .env template for Cro bot\n"
        "# Copy this to .env and edit the values\n\n"
        "DISCORD_TOKEN=your-bot-token-here\n"
        "BOT_MASTERS=123456789012345678,987654321098765432\n"
        "STEAM_API_KEY=\n"
        "TWITCH_CLIENT_ID=\n"
        "TWITCH_CLIENT_SECRET=\n"
        "YOUTUBE_API_KEY=\n"
    )

    p.write_text(content, encoding='utf-8')


__all__ = [
    'TOKEN', 'BOT_MASTERS', 'STEAM_API_KEY', 'TWITCH_CLIENT_ID',
    'TWITCH_CLIENT_SECRET', 'YOUTUBE_API_KEY', 'validate', 'create_env_template'
]
