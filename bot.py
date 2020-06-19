import asyncio
import os
import json
import discord

from discord.ext import commands
from scaler import slave

from utils.logger import Logger

with open('configs/bot_config.json', 'r') as file:
    settings = json.load(file)

# Some constants we need to define before everything else.
DEFAULT_PREFIX = settings.get("prefix", "vc/")
TOKEN = settings.get("token")
DEVELOPER_IDS = settings.get("dev_ids")
COLOUR = 0xe87e15
ICON = "https://cdn.discordapp.com/app-icons/656598065532239892/39344a26ba0c5b2c806a60b9523017f3.png"


class MyBot(commands.Bot, slave.Slave):
    """ This is a slave bot class, YOU DO NOT CONTROL SHARDS IN THIS FILE """
    def __init__(self, **options):
        # id_range = self.shard_ids_from_cluster()
        # options['shard_ids'] = id_range
        # options['shard_count '] = self.TOTAL_SHARDS
        super().__init__("", **options)

        self.ready_already = False

    def startup(self):
        """ Loads all the commands listed in cogs folder, if there isn't a cogs folder it makes one """
        if not os.path.exists('cogs'):
            os.mkdir('cogs')

        cogs_list = os.listdir('cogs')
        if '__pycache__' in cogs_list:
            cogs_list.remove('__pycache__')

        for cog in cogs_list:
            try:
                self.load_extension(f"cogs.{cog.replace('.py', '')}")
                Logger.log_info(f"Loaded Extension {cog.replace('.py', '')}")
            except Exception as e:
                print(f"Failed to load cog {cog}, Error: {e}")

    async def on_ready_once(self):
        await self.wait_until_ready()

    async def on_shard_ready(self, shard_id):
        Logger.log_shard_connect(shard_id)
        if not self.ready_already:
            self.ready_already = True
            await self.on_ready_once()

    async def get_custom_prefix(self, message: discord.Message):
        """ Fetches guild data either from cache or fetches it """
        return DEFAULT_PREFIX

    async def on_message(self, message):
        """ Used for case insensitive prefix """
        if not self.is_ready() or message.author.bot:
            return

        prefix = await self.get_custom_prefix(message)
        if message.content.lower().startswith(prefix.lower()):
            message.content = message.content[len(prefix):]
            await self.process_commands(message=message)

        elif message.content.startswith(f"<@{self.user.id}> "):
            message.content = message.content[len(f"<@{self.user.id}> "):]
            await self.process_commands(message=message)

        elif message.content.startswith(f"<@!{self.user.id}> "):
            message.content = message.content[len(f"<@!{self.user.id}> "):]
            await self.process_commands(message=message)


if __name__ == "__main__":
    bot = MyBot(case_insensitive=True, fetch_offline_member=False)
    bot.startup()
    bot.run(str(os.getenv("BOT_TOKEN")))
