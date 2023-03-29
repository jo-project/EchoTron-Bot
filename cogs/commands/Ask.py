from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from classes.embed import EmbedBuilder
from classes.client import Client
from classes.utilities import channel_check, convert_color

import openai
import os

openai.api_key = os.getenv("OPENAI_KEY")

class Ask(commands.Cog, name="ask"):
    def __init__(self, client: Client):
        self.client = client
        self.channel_id = 1090342512947896433
        
    @commands.hybrid_command(
        name="ask", 
        description="Ask OpenAI",
        with_app_command=True
    )
    @channel_check(1090342512947896433)
    @app_commands.describe(question='Question you want to ask')
    async def ask(self, ctx: Context, question: str):
        msg = await ctx.send(content=f"**{ctx.author.name}#{ctx.author.discriminator}**: {question}")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an assistant that is super good at programming. You alwasys explain every single detail of a function. You always format code using markdown like in discord"}, {"role": "user", "content": f"{question}"}]
        )
        res = completion.choices[0].message['content']
        await ctx.channel.send(content=res, reference=msg)
        
    
    @ask.error
    async def ask_error(self, ctx: Context, error):
        if isinstance(error, commands.CheckFailure):
            embed = EmbedBuilder()
            embed.set_title('Error')
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
            embed.set_description(description=f"This channel is only accessible on <#{self.channel_id}>")
            embed.set_color(convert_color('#ff8989'))
            
            await ctx.send(embed=embed)
        
        
async def setup(client: Client):
    await client.add_cog(Ask(client))