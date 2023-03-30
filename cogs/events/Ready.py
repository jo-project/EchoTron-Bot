from discord import __version__ as discord_version
import discord
from discord.ext import commands
import os

from classes.client import Client

class Ready(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener(name='on_ready')
    async def on_ready(self):
        self.client.log(name= self.client.user, version=discord_version, guild= len(self.client.guilds), user= len(self.client.users))

async def setup(client: Client):
    await client.add_cog(Ready(client))