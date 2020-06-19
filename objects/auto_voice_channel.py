import importlib
import inspect
import discord

from discord.ext import commands
from options.options import Template

class BaseAutoVoiceChannel:
    def __init__(self, guild: discord.Guild, channel_id: int):
        self._guild = guild
        self._channel_id = channel_id
        self._channel: discord.VoiceChannel = list(
            filter(None, [vc if vc.id == channel_id else False for vc in guild.voice_channels]))[0]
        self._template = Template(guild.id, channel_id)
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

    @property
    def id(self):
        return self.channel.id

    @property
    def member_count(self):
        return len(self.channel.members)

    async def delete(self, **kwargs):
        await self.channel.delete(**kwargs)

    async def rename(self, type_, *args, **kwargs):
        if self.template.needed_types.get(type_):
            new_name = self.template.get_name(*args, **kwargs)

