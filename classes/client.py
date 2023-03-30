from datetime import datetime
from discord import AppInfo, Message
from discord.ext import commands
from halo import Halo
from classes.database import Database
from termcolor import colored
import time

class Client(commands.AutoShardedBot):
    appInfo: AppInfo
    prefixes: dict = dict()
    uptime: datetime = datetime.now()
    database: Database
    
    def __init__(self, **kwargs):
        kwargs.pop('command_prefix', None)
        command_prefix = self.__prefix_callable
        super().__init__(command_prefix=command_prefix, **kwargs)
        
    def log(self, name: str, guild: int, user: int, version: str):
        data_list = [
            { "name": "Discord", "color": "cyan", "pre": f"Logging in...", "finish": f"Logged in as {name}", "loaded": False },
            { "name": "Database", "color": "green", "pre": f"Logging in...", "finish": f"Logged in as {self.database.db.name}", "loaded": False },
            { "name": "Version", "color": "blue", "pre": f"Fetching info...", "finish": f"Version {version}", "loaded": False },
            { "name": "Guilds", "color": "magenta", "pre": f"Fetching info...", "finish": f"{guild} guild(s)", "loaded": False },
            { "name": "Users", "color": "white", "pre": f"Fetching info...", "finish": f"{user} user(s)", "loaded": False },
        ]
        
        spinner = Halo(text="", spinner="dots")
        for data in data_list:
            text = data['pre']
            coloredText = lambda x: colored(x, data['color'], attrs=['bold'])
            spinner.text = f"[{coloredText(data['name'])}] {text}"
            spinner.start()
            time.sleep(1.5)
            data['loaded'] = True
            spinner.succeed(f"[{coloredText(data['name'])}] {data['finish']}")
            
    def log_command_sync(self, amount: int):
        text = f"Syncing..."
        coloredText = lambda x: colored(x, "white", attrs=['bold'])
        spinner = Halo(text="", spinner="dots")
        spinner.text = f"[{coloredText('Commands')}] {text}"
        spinner.start()
        time.sleep(1.5)
        spinner.succeed(f"[{coloredText('Commands')}] {amount} command(s)")
        
    def log_message(self, message: str):
        print(f"{message}")
        
    def __prefix_callable(self, client, message: Message):
        return commands.when_mentioned_or('?')(client, message)
    
    def loginDatabase(self):
        self.database = Database()
        name = self.database.getName()
        return name
        
    async def setup_hook(self):
        self.loginDatabase()
        self.appInfo = await self.application_info()
        
    async def close(self):
        await super().close()