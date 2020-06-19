"""

All options for the voice channels go here, the system automatically
loads them and assigns them when loading from a dict.

"""
import asyncio
from objects.option_manager import OptionManager
from objects.auto_voice_channel import AutoVoiceChannel


@OptionManager.avc_option(name="default_limit", description="sets a default limit to secondaries")
class DefaultLimit:
    def __init__(self, unloaded_dict: dict):
        self.default_limit = unloaded_dict.get('default_limit')

    def update(self, new):
        self.default_limit = new.get('default_limit')

    def unload(self):
        return self.__dict__

    async def apply(self, auto_voice_channel: AutoVoiceChannel, *args, **kwargs) -> AutoVoiceChannel:
        return auto_voice_channel


@OptionManager.avc_option(name="apply_template", description="Wow")
class ApplyTemplate:
    def __init__(self, unloaded_dict: dict):
        self.template = unloaded_dict.get('template')

    def update(self, new):
        self.template = new.get('template')

    def unload(self):
        return self.__dict__

    async def apply(self, auto_voice_channel: AutoVoiceChannel, *args, **kwargs) -> AutoVoiceChannel:
        return auto_voice_channel


if __name__ == '__main__':
    async def main():
        opt = DefaultLimit({})
        print(OptionManager.options)

    asyncio.run(main())
