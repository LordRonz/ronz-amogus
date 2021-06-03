from discord.ext import commands
from utils.add_reaction import flushed
from utils.triv import get_trivia, Triv

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='trivia', aliases=['triv'])
    @commands.cooldown(1, 6.9, commands.BucketType.guild)
    @commands.guild_only()
    async def trivia(self, ctx):
        '''Answer some trivia!'''

        async with ctx.typing():
            await flushed(ctx.message)
            triv: Triv = await get_trivia()

        if not triv:
            await ctx.send('`**ERROR**: Something went wrong`')
            return



def setup(bot):
    bot.add_cog(Games(bot))
