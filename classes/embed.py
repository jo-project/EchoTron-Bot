import pymongo
import os
import discord
from datetime import datetime

from typing import List, TypedDict, Optional
from discord.ext.commands import ColourConverter

class Field(TypedDict):
    name: str
    value: str
    inline: Optional[bool]

class EmbedBuilder(discord.Embed):
    def __init__(self):
        super().__init__()
        
    def set_title(self, title: str):
        self.title = title
        return self
        
    def set_description(self, description: str):
        self.description = description
        return self
    
    def set_timestamp(self, timestamp: datetime = datetime.now()):
        self.timestamp = timestamp
        return self
    
    def add_fields(self, *fields: List[Field]):
        for field in fields:
            name = field['name']
            value = field['value']
            inline = field.get('inline', False)
            self.add_field(name=name, value=value, inline=inline)
        return self
    
    def set_color(self, args):
        self.color = args
        return self