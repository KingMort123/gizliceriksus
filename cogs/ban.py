import discord
from discord.ext import commands
import random

class ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member} sunucudan yasaklandı.")

async def setup(bot):
    await bot.add_cog(ban(bot))