from datetime import datetime
from discord import __version__ as discord_version
from discord import AppInfo, Message
from discord.ext import commands
from logging import Logger
from logging import INFO as LOG_INFO
from typing import List
from halo import Halo
import time

class Client(commands.Bot):
    appInfo: AppInfo
    prefixes: dict = dict()
    uptime: datetime = datetime.now()
    
    def __init__(self, **kwargs):
        kwargs.pop('command_prefix', None)
        command_prefix = self.__prefix_callable
        super().__init__(command_prefix=command_prefix, **kwargs)
        
    def log(self, name: str, guild: int, user: int, version: str):
        data_list = [
            { "pre": f"Logging in...", "finish": f"Logged in as {name}", "loaded": False },
            { "pre": f"Getting version", "finish": f"Version {version}", "loaded": False },
            { "pre": f"Fetching guilds", "finish": f"{guild} guild(s)", "loaded": False },
            { "pre": f"Fetching users", "finish": f"{user} user(s)", "loaded": False },
        ]
        
        spinner = Halo(text="", spinner="dots")
        for data in data_list:
            spinner.text = data['pre']
            spinner.start()
            time.sleep(1.5)
            data['loaded'] = True
            spinner.succeed(data['finish'])
        
    def log_message(self, message: str):
        print(f"{message}")
        
    def __prefix_callable(self, client, message: Message):
        return commands.when_mentioned_or('?')(client, message)
    
    async def on_ready(self):
        self.log(name= self.user, version=discord_version, guild= len(self.guilds), user= len(self.users))
        
    async def setup_hook(self):
        self.appInfo = await self.application_info()
        
    async def close(self):
        await super().close()