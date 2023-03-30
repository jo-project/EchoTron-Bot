import time
import subprocess

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from classes.embed import EmbedBuilder
from classes.client import Client
from classes.utilities import random_color,channel_check, convert_color

class Terminal(commands.Cog, name="terminal"):
    def __init__(self, client: Client):
        self.client = client
        self.channel_id = 1090608626349113464
        
    @commands.hybrid_command(
        name="terminal", 
        description="Run command on terminal",
        with_app_command=True
    )
    @channel_check(1090608626349113464)
    @app_commands.describe(command = "Write your command to be executed on terminal")
    async def terminal(self, ctx: Context, command: str):
        before_time = time.perf_counter()
        await ctx.defer()
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=10)
            end_time = round(time.perf_counter() - before_time)
            embed = EmbedBuilder()
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
            embed.set_color(random_color())
            embed.set_title('Terminal')
            embed.set_description(f'```{result.decode("utf-8")}```')
            embed.set_timestamp()
            embed.set_footer(text=f"{self.client.user.name} | Executed in {end_time}ms", icon_url=self.client.user.display_avatar.url)
            return await ctx.reply(embed=embed)   
        except subprocess.CalledProcessError as e:
            errEmbed = EmbedBuilder()
            errEmbed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
            errEmbed.set_color(convert_color('#ff8989'))
            errEmbed.set_title('Terminal')
            errEmbed.set_description(f'```Error: {e.output.decode("utf-8")}```')
            return await ctx.reply(embed=errEmbed)
        except subprocess.TimeoutExpired:
            errEmbed = EmbedBuilder()
            errEmbed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
            errEmbed.set_color(convert_color('#ff8989'))
            errEmbed.set_title('Terminal')
            errEmbed.set_description(f'```Error: Command timed out.```')
            return await ctx.reply(embed=errEmbed)
    
    @terminal.error
    async def terminal_error(self, ctx: Context, error):
        if isinstance(error, commands.CheckFailure):
            embed = EmbedBuilder()
            embed.set_title('Error')
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
            embed.set_description(description=f"This channel is only accessible on <#{self.channel_id}>")
            embed.set_color(convert_color('#ff8989'))
            
            await ctx.send(embed=embed)
        
        
async def setup(client: Client):
    await client.add_cog(Terminal(client))