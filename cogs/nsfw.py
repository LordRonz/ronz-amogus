from discord.ext import commands
import discord
import asyncio
from random import choice
from utils.no_horny import holy_stuff, holy_quotes

def truncate(x: str, n: int):
    if len(x) < n:
        return x
    return x[0 : n - 4] + '...'

class Nsfw(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='nhentai')
    @commands.cooldown(1, 7.77, commands.BucketType.guild)
    @commands.guild_only()
    async def nhentai(self, ctx: commands.Context, id :str=''):
        '''BONK!'''
        await self.no_horny(ctx)

    @commands.command(name='r34', aliases=['rule34'])
    @commands.cooldown(1, 7.77, commands.BucketType.guild)
    @commands.guild_only()
    async def rule34(self, ctx: commands.Context):
        '''BONK!'''
        await self.no_horny(ctx)

    @commands.command(name='hentaigif')
    @commands.cooldown(1, 7.77, commands.BucketType.guild)
    @commands.guild_only()
    async def hentaigif(self, ctx: commands.Context):
        '''BONK!'''
        await self.no_horny(ctx)

    @commands.command(name='hentai')
    @commands.cooldown(1, 7.77, commands.BucketType.guild)
    @commands.guild_only()
    async def hentai(self, ctx: commands.Context):
        '''BONK!'''
        await self.no_horny(ctx)

    @commands.command(name='4k')
    @commands.cooldown(1, 7.77, commands.BucketType.guild)
    @commands.guild_only()
    async def four_k(self, ctx: commands.Context):
        '''BONK!'''
        await self.no_horny(ctx)

    @commands.command(name='agw', aliases=['asiansgonewild'])
    @commands.cooldown(1, 7.77, commands.BucketType.guild)
    @commands.guild_only()
    async def agw(self, ctx: commands.Context):
        '''BONK!'''
        await self.no_horny(ctx)

    @commands.command(name='gw', aliases=['gonewild'])
    @commands.cooldown(1, 7.77, commands.BucketType.guild)
    @commands.guild_only()
    async def gw(self, ctx: commands.Context):
        '''BONK!'''
        await self.no_horny(ctx)

    @commands.command(name='sauce', aliases=['soz'])
    @commands.cooldown(1, 7.77, commands.BucketType.guild)
    @commands.guild_only()
    async def sauce(self, ctx: commands.Context, *, url=''):
        '''BONK!'''
        await self.no_horny(ctx)

    async def no_horny(self, ctx: commands.Context):
        embed = discord.Embed(title=choice(holy_quotes), url='https://www.reddit.com/r/NoFap/', color=0x00ff00)

        embed.set_image(url=choice(holy_stuff))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Nsfw(bot))