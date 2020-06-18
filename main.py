import logging

from scaler.manage import SlaveManager

logging.basicConfig(level=logging.INFO)

class MyBotManager(SlaveManager):
    def __init__(self, target, shards, **kwargs):
        super().__init__(target, shards, **kwargs)

    def on_console_log(self, slave, content):
        print(content)


manager = MyBotManager(target="bot.py", shards=2, scale=2)
manager.run()
