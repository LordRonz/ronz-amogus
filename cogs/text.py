from discord.ext import commands
from utils.add_reaction import flushed
from random import choice
import requests

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open(f'./profanities/profanities.txt', 'r') as f:
            self.profanities = f.readlines()

        self.gooba_lyrics = requests.get('http://gist.githubusercontent.com/LordRonz/da8dcbf4cfdd07a19f239f5f6f555299/raw/4e9480c4a2fd8621dc9102b0e72ccf185575e95d/gooba.txt').text

    @commands.Cog.listener('on_message')
    async def sus(self, message):
        if message.author == self.bot.user or message.author.bot or not message.guild:
            return
        if 'sus' in message.content.lower():
            await flushed(message)
            await message.channel.send('**A M O G U S**')

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

def setup(bot):
    bot.add_cog(Text(bot))