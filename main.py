import discord
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

from classes.client import Client
from classes.utilities import clean_close, cogs_manager, cogs_directory

import json
config_file = open('config.json')


class Bot(Client):
    config: json.load(config_file)
    def __init__(self, **kwargs):
        super().__init__(
            activity=discord.Game(name="discord.gg/uckGjFUvec"),
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
        
        # Log it
        self.log_command_sync(len(synced))

    async def setup_hook(self):
        """Initialize the bot, database, prefixes & cogs."""
        await super().setup_hook()
        
        cogs = []
        for foldername in os.listdir(cogs_directory):
            folder_path = os.path.join(cogs_directory, foldername)
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    if filename.lower().endswith(".py"):
                        cogs.append(f"cogs.{foldername}.{filename[:-3]}")
        await cogs_manager(self, "load", cogs)

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
