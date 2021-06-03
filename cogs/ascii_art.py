from discord.ext import commands
from utils.add_reaction import flushed
from random import choice

class ASCIIart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        temp_amoguses = []
        AMOGUS_COUNT = 7
        for i in range(AMOGUS_COUNT):
            with open(f'./amoguses/amogus{i}.txt', 'r') as f:
                temp_amoguses.append(f.read())

        self.amoguses = (*temp_amoguses,)

        with open(f'./random_txt/nice_cock.txt', 'r') as f:
            self.nice_cock = f.read()

        with open(f'./random_txt/zukowei.txt', 'r') as f:
            self.zukowei = f.read()

    @commands.command(name='amogus', aliases=['amongus'])
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.guild_only()
    async def amogus(self, ctx):
        '''When the impostor is sus 😳'''

        await flushed(ctx.message)
        await ctx.send(choice(self.amoguses))

    @commands.command(name='cock', aliases=['dong', 'schlong', 'dick'])
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.guild_only()
    async def cock(self, ctx):
        '''Nice cock bro'''

        await flushed(ctx.message)
        await ctx.send(self.nice_cock)

    @commands.command(name='yntkts')
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.guild_only()
    async def yntkts(self, ctx):
        '''YO NDAK TAU KOK TANYA SAYA'''

        await flushed(ctx.message)
        await ctx.send(self.zukowei)

def setup(bot):
    bot.add_cog(ASCIIart(bot))
