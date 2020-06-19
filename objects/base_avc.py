import discord
from discord.ext import commands

from objects.option_manager import OptionManager, BaseOption

class BaseAutoVoiceChannel:
    def __init__(self, guild: discord.Guild, channel_id: int):
        self._guild = guild
        self._channel_id = channel_id


class AVCOptions:
    def __init__(self, base_options=None):
        if base_options is None:
            base_options = []
        for option in base_options:
            setattr(self, str(option), option)

    def to_dict(self):
        items = {}
        for key, value in self.__dict__.items():
            if hasattr(value, 'unload'):
                data = getattr(value, 'unload')()
                items[key] = data
        return items

    def from_dict(self, options_dict: dict):
        for name, value in options_dict.items():
            option = OptionManager.options.get(name)
            if option is not None:
                option = option(value)
                setattr(self, name, option)
        return self


if __name__ == "__main__":
    from options.options import *
    test = AVCOptions()
    test = test.from_dict({'default_limit': {'default_limit': 1}})
    print(test.to_dict())