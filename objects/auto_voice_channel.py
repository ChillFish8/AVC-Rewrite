import importlib
import inspect
import discord
from discord.ext import commands

from objects.base_avc import BaseAutoVoiceChannel

class AutoVoiceChannel(BaseAutoVoiceChannel):
    def __init__(self, guild: discord.Guild, channel_id: int):
        super().__init__(guild, channel_id)


