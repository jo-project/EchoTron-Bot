from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from classes.embed import EmbedBuilder
from classes.client import Client
from classes.utilities import channel_check, convert_color
from classes.openai import generate_answer, generate_image, generate_image_replica

import json

config_file = open('config.json')
config = json.load(config_file)

class AI(commands.Cog, name="ai"):
    def __init__(self, client: Client):
        self.client = client
        
    @commands.hybrid_command(
        name="ask", 
        description="Ask OpenAI",
        with_app_command=True
    )
    @channel_check(1090604466920751124)
    @app_commands.describe(question='Question you want to ask')
    async def ask(self, ctx: Context, question: str):
        msg = await ctx.send(content=f"**{ctx.author.name}#{ctx.author.discriminator}**: {question}")
        answer = await generate_answer(question)
        await ctx.channel.send(content=answer, reference=msg)
        
    @commands.hybrid_command(
        name="draw", 
        description="Generate image using AI",
        with_app_command=True
    )
    @channel_check(1090604897252151316)
    @app_commands.describe(type='Type of generator',prompt='Prompt an image to generate')
    @app_commands.choices(type=[
        app_commands.Choice(name='Dall•E', value="dalle"),
        app_commands.Choice(name='Diffusion', value='diffusion'),
        app_commands.Choice(name='OpenJourney', value='openjourney')
    ])
    async def draw(self, ctx: Context, prompt: str, type: str = 'dalle'):
        msg = await ctx.defer()
        if type == 'dalle':
            generator = 'Dall•E'
            image = await generate_image(ctx.author.name, prompt)
        elif type == 'diffusion':
            generator = 'Diffusion'
            image = await generate_image_replica(ctx.author.name, prompt, 'diffusion')
        elif type == 'openjourney':
            generator = 'OpenJourney'
            image = await generate_image_replica(ctx.author.name, prompt, 'openjourney')
            
        await ctx.reply(content=f"**{prompt}** - <@{ctx.author.id}> ({generator})", file=image)
        
    
    @ask.error
    async def ask_error(self, ctx: Context, error):
        if isinstance(error, commands.CheckFailure):
            embed = EmbedBuilder()
            embed.set_title('Error')
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
            embed.set_description(description=f"This channel is only accessible on <#{config['channels']['ask']}>")
            embed.set_color(convert_color('#ff8989'))
            
            await ctx.send(embed=embed)
            
    @draw.error
    async def draw_error(self, ctx: Context, error):
        if isinstance(error, commands.CheckFailure):
            embed = EmbedBuilder()
            embed.set_title('Error')
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
            embed.set_description(description=f"This channel is only accessible on <#{config['channels']['draw']}>")
            embed.set_color(convert_color('#ff8989'))
            
            await ctx.send(embed=embed)
        
        
async def setup(client: Client):
    await client.add_cog(AI(client))