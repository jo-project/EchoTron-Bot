import time

from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed, app_commands

from classes.client import Client
from classes.utilities import channel_check, convert_color, random_color
from classes.embed import EmbedBuilder

class Purge(commands.Cog, name="purge"):
    def __init__(self, client: Client):
        self.client = client
    
    @commands.hybrid_command(
        name="purge", 
        description="Delete a number of messages",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @app_commands.describe(amount="The amount of messages that should be deleted")
    async def purge(self, ctx: Context, amount: int):
        before_time = time.perf_counter()
        await ctx.defer(
            ephemeral= True
        )
        purged_messages = await ctx.channel.purge(limit=amount + 1)
        end_time = round((time.perf_counter() - before_time) * 1000)
        print(end_time)
        
        embed = EmbedBuilder()
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
        embed.set_title('Purge')
        embed.set_description(f"Cleared **{len(purged_messages) - 1}** messages!")
        embed.set_color(random_color())
        embed.set_timestamp()
        embed.set_footer(text=f"{self.client.user.name} | Executed in {end_time}ms", icon_url=self.client.user.display_avatar.url)
        
        await ctx.reply(embed=embed)
        
        
        
async def setup(client: Client):
    await client.add_cog(Purge(client))