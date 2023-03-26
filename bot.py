import discord
import logging
import os

from dotenv import load_dotenv
from classes.client import Client
from classes.utilities import clean_close, cogs_manager, cogs_directory

from os import listdir

from keep_alive import keep_alive

load_dotenv()


class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(
            activity=discord.Game(name="Booting.."),
            allowed_mentions=discord.AllowedMentions(everyone=False),
            case_insensitive=True,
            intents=kwargs.pop("intents", discord.Intents.all()),
            max_messages=2500,
            status=discord.Status.online,
            **kwargs,
        )

    async def startup(self):
        """Sync application commands"""
        await self.wait_until_ready()

        # Sync application commands
        synced = await self.tree.sync()
        self.log_message(f"Application commands synced ({len(synced)})")

    async def setup_hook(self):
        """Initialize the bot, database, prefixes & cogs."""
        await super().setup_hook()

        # Cogs loader
        cogs = [f"cogs.{filename[:-3]}" for filename in listdir(
            cogs_directory) if filename.endswith(".py")]
        await cogs_manager(self, "load", cogs)
        self.log_message(f"Cogs loaded ({len(cogs)}): {', '.join(cogs)}")

        # Sync application commands
        self.loop.create_task(self.startup())


if __name__ == '__main__':
    clean_close()  # Avoid Windows EventLoopPolicy Error
    keep_alive()
    title = "EchoTron" # The title you want to set for the WSL tab
    os.system(f'echo -ne "\\033]0;{title}\\007"')
    os.system('clear')
    bot = Bot()
    bot.run(
        os.getenv("TOKEN"),
        reconnect=True,
        log_handler=None,
    )
