from discord.ext import commands
from utils.add_reaction import flushed
from utils.cataas import get_cat
from utils.dogaas import get_doggo

class Animal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cat', aliases=['pussy', 'kitty', 'meow'])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def cat(self, ctx):
        '''Lets see some pussies!'''

        await flushed(ctx.message)
        await ctx.send(await get_cat())

    @commands.command(name='dog', aliases=['doggo', 'puppy', 'bork'])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def dog(self, ctx):
        '''Bork Bork! 🐶'''

        await flushed(ctx.message)
        await ctx.send(await get_doggo())

def setup(bot):
    bot.add_cog(Animal(bot))
