import time

from os import listdir, path
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

from classes.utilities import clean_close, cogs_manager, cogs_directory, channel_check

from classes.client import Client

class Dev(commands.Cog, name="test"):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_group(invoke_without_command=True)
    @channel_check(1090608626349113464)
    async def dev(self, ctx: Context):
        pass
    
    @dev.group(
        name="reload", 
        description="Reload command",
    )
    async def reload(self, ctx: Context):
        pass
    
    @reload.command(name="all", description="reload all") 
    async def all(self, ctx: Context):
        cogs = []
        for foldername in listdir(cogs_directory):
            folder_path = path.join(cogs_directory, foldername)
            if path.isdir(folder_path):
                for filename in listdir(folder_path):
                    if filename.lower().endswith(".py"):
                        cogs.append(f"cogs.{foldername}.{filename[:-3]}")
                        
        await cogs_manager(self.client, "reload", cogs)     
            
    @reload.command(name="event", description="Reload events")
    @app_commands.describe(event='Event that you want to reload (default all)')
    async def event(self, ctx: Context, event: str = 'all'):
        if event == 'all':
            cogs = []
            folder_path = path.join(cogs_directory, 'events')
            if path.isdir(folder_path):
                for filename in listdir(folder_path):
                    if filename.lower().endswith(".py"):
                        cogs.append(f"cogs.events.{filename[:-3]}")
        else:
            cogs = []
            folder_path = path.join(cogs_directory, 'events')
            if path.isdir(folder_path):
                for filename in listdir(folder_path):
                    if filename.lower().endswith(".py") and filename[:-3].lower() == event.lower():
                        cogs.append(f"cogs.events.{filename[:-3]}")
                        
        await cogs_manager(self.client, "reload", cogs)
        
    @reload.command(name="command", description="Reload commands")
    async def command(self, ctx: Context, command: str = 'all'):
        if command == 'all':
            cogs = []
            folder_path = path.join(cogs_directory, 'commands')
            if path.isdir(folder_path):
                for filename in listdir(folder_path):
                    if filename.lower().endswith(".py"):
                        cogs.append(f"cogs.commands.{filename[:-3]}")
        else:
            cogs = []
            folder_path = path.join(cogs_directory, 'commands')
            if path.isdir(folder_path):
                for filename in listdir(folder_path):
                    if filename.lower().endswith(".py") and filename[:-3].lower() == command.lower():
                        cogs.append(f"cogs.commands.{filename[:-3]}")
                        
        await cogs_manager(self.client, "reload", cogs)
        
        
        
async def setup(client: Client):
    await client.add_cog(Dev(client))