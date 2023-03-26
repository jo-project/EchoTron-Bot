import time

from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed

from classes.client import Client

class Ping(commands.Cog, name="ping"):
    def __init__(self, client):
        self.client = client
        
    @commands.hybrid_command(
        name="ping", 
        description="Ping command",
        with_app_command=True
    )
    async def ping(self, ctx: Context):
        before = time.monotonic()
        await ctx.defer()
        bot_latency = round(self.client.latency * 1000)
        ping = int((time.monotonic() - before) * 1000)
        embed = Embed(title="Ping")
        embed.set_author(name=ctx.me, icon_url=ctx.me.avatar)
        embed.add_field(name="API Latency", value=f"`{bot_latency}ms`", inline=True)
        embed.add_field(name="Bot Latency", value=f"`{ping}ms`", inline=True)
        await ctx.reply(embed=embed)
        
        
async def setup(client: Client):
    await client.add_cog(Ping(client))