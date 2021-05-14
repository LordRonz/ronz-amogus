from discord.ext import commands
import discord

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listguild', hidden=True)
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.is_owner()
    @commands.guild_only()
    async def list_guild(self, ctx):
        guilds = '\n'.join(f'{guild.name} {guild.id}' for guild in self.bot.guilds)
        e = discord.Embed(title='Joined Guilds', color=0xff0000, description=guilds)
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Owner(bot))