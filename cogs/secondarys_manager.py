import discord

from discord.ext import commands
from data.cache import Cache

from objects.auto_voice_channel import SecondaryAVChannel

class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.secondaries = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member,
                                    before: discord.VoiceState, after: discord.VoiceState):
        if before.channel is None and after.channel is not None:
            await self.make_secondary(member, after)
        if before.channel is not None and after.channel is None:
            await self.check_delete(before, after)

    async def make_secondary(self, member, voice):
        if Cache.auto_voice_channels.get(voice.channel.id):
            secondary: SecondaryAVChannel = await Cache.auto_voice_channels.get(voice.channel.id).new(member=member)
            self.secondaries[secondary.id] = secondary
            await member.move_to(secondary.channel, reason="Moving to secondary")

    async def check_delete(self, before, after):
        if self.secondaries.get(before.channel.id):
            channel: SecondaryAVChannel = self.secondaries.get(before.channel.id)
            if channel.member_count <= 0:
                await channel.delete(reason="No members in channel")
            else:
                await channel.rename(context={'vc_before': before, 'vc_after': after})

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        state: discord.VoiceState = after.voice
        if state.channel is None:
            return
        elif self.secondaries.get(state.channel.id):
            secondary: SecondaryAVChannel = self.secondaries.get(state.channel.id)
            await secondary.rename(context={'user_before': before, 'user_after': after})



def setup(bot):
    bot.add_cog(OwnerCommands(bot))


if __name__ == "__main__":
    test = OwnerCommands("wow")
