import time
import datetime
from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed
import random

from classes.embed import EmbedBuilder
from classes.client import Client
from classes.utilities import random_color,channel_check, convert_color

class Ping(commands.Cog, name="ping"):
    def __init__(self, client: Client):
        self.client = client
        self.channel_id = 1090608626349113464
        
    @commands.hybrid_command(
        name="ping", 
        description="Ping command",
        with_app_command=True
    )
    @channel_check(1090608626349113464)
    async def ping(self, ctx: Context):
        before = time.monotonic()
        before_time = time.perf_counter()
        await ctx.defer()
        bot_latency = round(self.client.latency * 1000)
        end_time = round((time.perf_counter() - before_time) * 1000)
        ping = int((time.monotonic() - before) * 1000)
        
        embed = EmbedBuilder()
        embed.set_title('Ping')
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
        embed.set_color(random_color())
        embed.add_fields(
            { 'name': 'API Latency', 'value': f"`{bot_latency}ms`", 'inline': True },
            { 'name': 'Bot Latency', 'value': f"`{ping}ms`", 'inline': True }
        )
        embed.set_timestamp()
        embed.set_footer(text=f"{self.client.user.name} | Executed in {end_time}ms", icon_url=self.client.user.display_avatar.url)
        
        await ctx.reply(embed=embed)
    
    @ping.error
    async def ping_error(self, ctx: Context, error):
        if isinstance(error, commands.CheckFailure):
            embed = EmbedBuilder()
            embed.set_title('Error')
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
            embed.set_description(description=f"This channel is only accessible on <#{self.channel_id}>")
            embed.set_color(convert_color('#ff8989'))
            
            await ctx.send(embed=embed)
        
        
async def setup(client: Client):
    await client.add_cog(Ping(client))