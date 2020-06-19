"""

All options for the voice channels go here, the system automatically
loads them and assigns them when loading from a dict.

"""
import asyncio

class Template:
    def __init__(self, guild_id: int, vc_id: int):
        self.guild_id = guild_id
        self.vc_id = vc_id

    def get_name(self, *args, **kwargs):
        return "bob"