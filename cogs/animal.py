from discord.ext import commands
from utils.add_reaction import flushed
from utils.cataas import get_cat

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

def setup(bot):
    bot.add_cog(Animal(bot))
