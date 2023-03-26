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

from classes.client import Client

root_directory = dirname(dirname(abspath(__file__)))
cogs_directory = join(root_directory, "cogs")

async def cogs_manager(bot: Client, mode: str, cogs: list[str]) -> None:
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

			bot.log_message(f"Cog {cog} {mode}ed")
		except Exception as e:
			raise e

def reload_views():
	mods = [module[1] for module in modules.items() if isinstance(module[1], ModuleType)]
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
			raise TypeError(f"Cannot decorate a class that is not a subclass of Command, get: {type(command)} must be Command")

		valid_required_permissions = [
			perm for perm, value in perms.items() if getattr(discord.Permissions.none(), perm) != value
		]
		command.extras.update({"bot_permissions": valid_required_permissions})

		if isinstance(command, commands.HybridCommand) and command.app_command:
			command.app_command.extras.update({"bot_permissions": valid_required_permissions})

		if isinstance(command, (app_commands.Command, commands.HybridCommand)):
			app_commands.checks.bot_has_permissions(**perms)(command)
		if isinstance(command, (commands.Command, commands.HybridCommand)):
			commands.bot_has_permissions(**perms)(command)

		return command

	return wrapped