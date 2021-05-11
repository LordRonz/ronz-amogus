from discord.ext import commands
from utils.add_reaction import flushed
from utils.yomomma import get_yomomma
from utils.emojifier import get_emojified_text
from random import choice
import requests

class Text(commands.Cog):
    _AMOGUS = '**A M O G U S**'
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1, 3, commands.BucketType.guild)


        with open(f'./profanities/profanities.txt', 'r') as f:
            self.profanities = f.readlines()

        self.gooba_lyrics = requests.get('http://gist.githubusercontent.com/LordRonz/da8dcbf4cfdd07a19f239f5f6f555299/raw/4e9480c4a2fd8621dc9102b0e72ccf185575e95d/gooba.txt').text

    def get_ratelimit(self, message):
        '''Returns the ratelimit left'''
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener('on_message')
    async def sus(self, message):
        if message.author == self.bot.user or message.author.bot or not message.guild:
            return
        if 'sus' in message.content.lower():
            ratelimit = self.get_ratelimit(message)
            if ratelimit:
                return
            await flushed(message)
            await message.channel.send(self._AMOGUS)

    @commands.command(name='swear')
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.guild_only()
    async def swear(self, ctx):
        '''Profanity is a socially offensive use of language, which may also be called cursing, cussing or swearing, cuss words (American English vernacular), curse words, swear words, bad words, dirty words, or expletives.'''

        await flushed(ctx.message)
        await ctx.send(choice(self.profanities))

    @commands.command(name='gooba')
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.guild_only()
    async def gooba(self, ctx):
        '''Gooba Lyrics'''

        await flushed(ctx.message)
        await ctx.send(self.gooba_lyrics)

    @commands.command(name='yomomma', aliases=['yomama'])
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.guild_only()
    async def yomomma(self, ctx):
        '''Random yo momma joke'''
        await flushed(ctx.message)
        joke = await get_yomomma()
        await ctx.send(joke)

    @commands.command(name='emojify')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    async def emojify(self, ctx, *, msg: str):
        '''Make the bot say whatever you want with emojis!'''
        await ctx.send(await get_emojified_text(msg))

def setup(bot):
    bot.add_cog(Text(bot))