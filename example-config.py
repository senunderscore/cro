import os
from typing import List

TOKEN: str = os.getenv('TOKEN', 'your-bot-token-here')

_masters = os.getenv('BOT_MASTERS', 'your-user-id-here')
BOT_MASTERS: List[str] = [m.strip() for m in _masters.split(',')]

STEAM_API_KEY: str = os.getenv('STEAM_API_KEY', '')

TWITCH_CLIENT_ID: str = os.getenv('TWITCH_CLIENT_ID', '')
TWITCH_CLIENT_SECRET: str = os.getenv('TWITCH_CLIENT_SECRET', '')

YOUTUBE_API_KEY: str = os.getenv('YOUTUBE_API_KEY', '')

if TOKEN == 'your-bot-token-here':
    raise ValueError("TOKEN is not configured. Set TOKEN environment variable or update config.py")

if not BOT_MASTERS or BOT_MASTERS == ['your-user-id-here']:
    print("WARNING: BOT_MASTERS not configured. Some admin commands will not work.")
