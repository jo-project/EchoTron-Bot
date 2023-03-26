import time

from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed, app_commands

from classes.client import Client

class Purge(commands.Cog, name="purge"):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Purge.py is ready!")
        
    @commands.hybrid_command(
        name="purge", 
        description="Purge command",
        with_app_command=True
    )
    @commands.is_owner()
    @app_commands.describe(amount="Amount of message you want to delete")
    async def purge(self, ctx: Context, amount: int):
        await ctx.defer()
        z = await ctx.channel.purge(limit=amount)
        
        
        
async def setup(client: Client):
    await client.add_cog(Purge(client))