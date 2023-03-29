import asyncio
import discord
import logging
import platform

from discord.ext import commands
from discord import app_commands

from importlib import reload
from json import load
from os import listdir
from os.path import dirname, abspath, join, basename, splitext
from sys import modules
from types import ModuleType
from typing import Union
import random
import re

from prettytable import PrettyTable

from classes.client import Client

root_directory = dirname(dirname(abspath(__file__)))
cogs_directory = join(root_directory, "cogs")


async def cogs_manager(bot: Client, mode: str, cogs: list[str]) -> None:
    x = PrettyTable()
    x.field_names = ['Cogs', 'Type', 'Mode']
    for cog in cogs:
        try:
            if mode == "unload":
                await bot.unload_extension(cog)
            elif mode == "load":
                await bot.load_extension(cog)
            elif mode == "reload":
                await bot.reload_extension(cog)
            else:
                raise ValueError("Invalid mode.")
            
            cogType = cog.split('.')[1]
            cogName = cog.split('.')[2]
            cogMode = f"{mode}ed".upper()
            x.add_row([cogName, cogType, cogMode])
        except Exception as e:
            raise e
    print(x)
    
def random_color() -> discord.Color:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return discord.Color.from_rgb(r, g, b)

def convert_color(color: str) -> discord.Color:
    hex_string = color.strip('#')
    hex_regex = re.compile('[0-9a-fA-F]{6}')
    if hex_regex.match(hex_string):
        rgb = tuple(int(hex_string[i:i+2], 16) for i in (0, 2, 4))
        return discord.Color.from_rgb(*rgb)
    else:
        raise ValueError(f"Invalid hex string: {hex_string}")

def channel_check(channel_id):
    async def predicate(ctx):
        return ctx.channel.id == channel_id
    return commands.check(predicate)


def reload_views():
    mods = [module[1]
            for module in modules.items() if isinstance(module[1], ModuleType)]
    for mod in mods:
        try:
            if basename(dirname(str(mod.__file__))) == "views":
                reload(mod)
                yield mod.__name__
        except:
            pass


def clean_close() -> None:
    if platform.system().lower() == 'windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def bot_has_permissions(**perms: bool):
    """A decorator that add specified permissions to Command.extras and add bot_has_permissions check to Command with specified permissions.

    Warning:
    - This decorator must be on the top of the decorator stack
    - This decorator is not compatible with commands.check()
    """
    def wrapped(command: Union[app_commands.Command, commands.HybridCommand, commands.Command]) -> Union[app_commands.Command, commands.HybridCommand, commands.Command]:
        if not isinstance(command, (app_commands.Command, commands.hybrid.HybridCommand, commands.Command)):
            raise TypeError(
                f"Cannot decorate a class that is not a subclass of Command, get: {type(command)} must be Command")

        valid_required_permissions = [
            perm for perm, value in perms.items() if getattr(discord.Permissions.none(), perm) != value
        ]
        command.extras.update({"bot_permissions": valid_required_permissions})

        if isinstance(command, commands.HybridCommand) and command.app_command:
            command.app_command.extras.update(
                {"bot_permissions": valid_required_permissions})

        if isinstance(command, (app_commands.Command, commands.HybridCommand)):
            app_commands.checks.bot_has_permissions(**perms)(command)
        if isinstance(command, (commands.Command, commands.HybridCommand)):
            commands.bot_has_permissions(**perms)(command)

        return command

    return wrapped
