import asyncio

from discord.ext import commands
from scaler import slave

from utils.logger import Logger

class MyBot(commands.Bot, slave.Slave):
    """ This is a slave bot class, YOU DO NOT CONTROL SHARDS IN THIS FILE """
    def __init__(self, command_prefix, **options):
        id_range = self.shard_ids_from_cluster()
        options['shard_ids'] = id_range
        options['shard_count '] = self.TOTAL_SHARDS
        super().__init__(command_prefix, **options)

        self.ready_already = False

    async def on_ready_once(self):
        await self.wait_until_ready()

    async def on_shard_ready(self, shard_id):
        Logger.log_shard_connect(shard_id)
        if not self.ready_already:
            self.ready_already = True
            await self.on_ready_once()


bot = MyBot(command_prefix="?")
if __name__ == "__main__":
    bot.run("NjQxMzgxNzYyNzg1NjA3Njk4.XuuNow.aTiEWVmabfLq0gjbPsg0gX-7CPY")