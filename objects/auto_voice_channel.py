import importlib
import inspect
import discord
import time
import asyncio

from discord.ext import commands
from datetime import  datetime, timedelta

from options.options import Template

VC_RENAME_RATE_LIMIT = 300  # Rename once per 5 minutes if applicable
DEFAULT_TEMPLATE = ""

class BaseAutoVoiceChannel:
    def __init__(self, guild: discord.Guild, channel_id: int):
        self._guild = guild
        self._channel_id = channel_id
        self._channel: discord.VoiceChannel = list(
            filter(None, [vc if vc.id == channel_id else False for vc in guild.voice_channels]))[0]

        self._options = {}
        self._template = Template(guild.id, channel_id, self._options.get('template', DEFAULT_TEMPLATE))
        self._active_channels = {}

    async def new(self, *args, **kwargs):
        name = self._template.get_name(*args, **kwargs)
        new = await self._channel.clone(name=name)
        self._active_channels[new.id] = SecondaryAVChannel(
            guild=kwargs.get('guild'),
            voice_channel=new,
            template=self._template
        )
        return self._active_channels[new.id]

    @property
    def active(self):
        return self._active_channels


class AutoVoiceChannel(BaseAutoVoiceChannel):
    """ This is a primary voice channel """
    def __init__(self, guild: discord.Guild, channel_id: int):
        super().__init__(guild, channel_id)


class SecondaryAVChannel:
    """ This is a secondary Voice channel """
    def __init__(self, guild, voice_channel, **kwargs):
        self.guild: discord.Guild = guild
        self.channel: discord.VoiceChannel = voice_channel
        self.template: Template = kwargs.get('template')
        self.last_edited = time.time()
        self.retry_handle = None

    @property
    def id(self):
        return self.channel.id

    @property
    def member_count(self):
        return len(self.channel.members)

    async def delete(self, **kwargs):
        await self.channel.delete(**kwargs)

    async def rename(self, context: dict):
        new_name = self.template.get_name(**context)
        if new_name == self.channel.name:
            return
        else:
            if self.last_edited + VC_RENAME_RATE_LIMIT < time.time():
                if self.retry_handle is not None:
                    self.retry_handle.cancel()
                await self.channel.edit(name=new_name)
                self.last_edited = time.time()
            else:
                loop = asyncio.get_event_loop()
                delta = loop.time() + (time.time() - self.last_edited + VC_RENAME_RATE_LIMIT)
                self.retry_handle = loop.call_at(delta, self.rename, context)


