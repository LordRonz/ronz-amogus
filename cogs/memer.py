import discord
from discord.ext import commands
from utils.add_reaction import flushed
from utils.reddit_handler import get_meme
from utils.xkcd import Xkcd

class Memer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xkcd_comic = Xkcd()
        url = 'https://cdn.discordapp.com/attachments/545749990472024125/841518852898947122/unknown.mp4'
        self.rick = f'**Definitely not a rickroll**\n{url}'

    @commands.command(name='meme')
    @commands.cooldown(1, 6.9, commands.BucketType.guild)
    @commands.guild_only()
    async def meme(self, ctx):
        '''
        Fetch random meme from r/dankmemes or r/memes
        '''

        async with ctx.typing():
            await flushed(ctx.message)
            meme = await get_meme()
            embed = discord.Embed(title=meme.title, url=meme.permalink, color=0xff0000)
            embed.set_image(url=meme.img)
            await ctx.send(embed=embed)

    @commands.command(name='xkcd')
    @commands.cooldown(1, 6.9, commands.BucketType.guild)
    @commands.guild_only()
    async def xkcd(self, ctx):
        '''
        Fetch random xkcd comic
        '''

        async with ctx.typing():
            await flushed(ctx.message)
            comic = await self.xkcd_comic.get()
            embed = discord.Embed(title=comic.title, url=comic.url, description=comic.desc, color=0xff0000)
            embed.set_image(url=comic.img)
            await ctx.send(embed=embed)

    @commands.command(name='rickroll', aliases=['rr'])
    @commands.cooldown(1, 6.9, commands.BucketType.guild)
    @commands.guild_only()
    async def rick_roll(self, ctx):
        '''
        Rolling rick
        '''

        await flushed(ctx.message)
        await ctx.send(self.rick)

def setup(bot):
    bot.add_cog(Memer(bot))