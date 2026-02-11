import discord
import asyncio
import random
import json
import logging
import os
from typing import List, Union

from dotenv import load_dotenv
from discord.ext import commands

from utils.settings.handler import ServerSettings

#################################
# Environment
#################################
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set in the .env file!")

#################################
# Logging
#################################
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#################################
# Bot Class
#################################
class Bot(commands.Bot):
    def __init__(self):
        self.default_prefixes = ['-', '?', '!', '.']

        super().__init__(
            command_prefix=self.get_prefix,
            intents=discord.Intents.all(),
            help_command=None,
        )

        self.settings = ServerSettings()

    #################################
    ## Setup Hook
    #################################
    async def setup_hook(self):
        logger.info("Loading core events...")
        for event in ['logging', 'messages', 'errors']:
            try:
                await self.load_extension(f"events.core.{event}")
                logger.info(f"Loaded events.core.{event}")
            except Exception as e:
                logger.exception(f"Failed to load events.core.{event}")

        logger.info("Loading feature events...")
        for event in ['starboard', 'tracking']:
            try:
                await self.load_extension(f"events.features.{event}")
                logger.info(f"Loaded events.features.{event}")
            except Exception as e:
                logger.exception(f"Failed to load events.features.{event}")

        logger.info("Loading cogs...")
        for extension in [
            "cogs.moderation",
            "cogs.admin",
            "cogs.casual",
            "cogs.fun",
            "cogs.help",
        ]:
            try:
                await self.load_extension(extension)
                logger.info(f"Loaded {extension}")
            except Exception as e:
                logger.exception(f"Failed to load {extension}")

    #################################
    ## Ready and Status
    #################################
    async def on_ready(self):
        logger.info(f"{self.user} is online!")

        status_messages = []
        try:
            with open("data/strings.json", "r", encoding="utf-8") as f:
                strings = json.load(f)
                status_messages = strings.get("status", []) if isinstance(strings, dict) else []
        except FileNotFoundError:
            logger.warning("data/strings.json not found; using default status message")
        except json.JSONDecodeError:
            logger.exception("Failed to parse data/strings.json; using default status message")

        await self.change_presence(
            status=discord.Status.idle,
            activity=discord.CustomActivity(
                name=random.choice(status_messages) if status_messages else "Online"
            ),
        )

        async def rotate_status():
            while True:
                await asyncio.sleep(30)
                await self.change_presence(
                    status=discord.Status.idle,
                    activity=discord.CustomActivity(
                        name=random.choice(status_messages) if status_messages else "Online"
                    ),
                )

        self.loop.create_task(rotate_status())

    #################################
    ## Get Prefix
    #################################
    async def get_prefix(self, message):
        if not message.guild:
            return self.default_prefixes

        settings = self.settings.get_all_server_settings(message.guild.id)
        prefixes = []

        custom_prefix = settings.get("prefix")
        if custom_prefix:
            prefixes.append(custom_prefix)

        if settings.get("use_default_prefix", True):
            prefixes.extend(self.default_prefixes)

        return prefixes if prefixes else self.default_prefixes


# ----------------------------------
# Entrypoint
# ----------------------------------
def main():
    bot = Bot()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
