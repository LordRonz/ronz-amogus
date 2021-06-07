from discord.ext import commands
import discord
import gc
from psutil import Process
from extensions import EXTENSIONS
from datetime import timedelta
from time import time

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = Process()
        self.start_time = time()

    @commands.command(name='listguild', hidden=True)
    @commands.is_owner()
    async def list_guild(self, ctx):
        guilds = '\n'.join(f'{guild.name} {guild.id}' for guild in self.bot.guilds)
        e = discord.Embed(title='Joined Guilds', color=0xff0000, description=guilds)
        await ctx.send(embed=e)

    @commands.command(name='guildcount', aliases=['guildcnt', 'servercount', 'servercnt'], hidden=True)
    @commands.is_owner()
    async def guild_cnt(self, ctx):
        count = len(self.bot.guilds)
        e = discord.Embed(title='Guild Count', color=0xff0000, description=f'**{count} {"guilds" if count > 1 else "guild"}**')
        await ctx.send(embed=e)

    @commands.command(name='usercount', aliases=['usercnt'], hidden=True)
    @commands.is_owner()
    async def user_cnt(self, ctx):
        count = len(self.bot.users)
        e = discord.Embed(title='User Count', color=0xff0000, description=f'**{count} {"users" if count > 1 else "user"}**')
        await ctx.send(embed=e)

    @commands.command(name='stats', aliases=['status', 'stat'], hidden=True)
    @commands.is_owner()
    async def stats(self, ctx):
        user_count = len(self.bot.users)
        guild_count = len(self.bot.guilds)
        cogs = '\n'.join(c for c in self.bot.cogs.keys())
        ram = f'{self.process.memory_info().vms / 1048576} MB'
        uptime = f'{timedelta(seconds=round(time() - self.start_time))}'

        e = discord.Embed(title=self.bot.user.name, color=0xff0000, description=f'ID: `{self.bot.user.id}`')

        e.add_field(name='Uptime', value=uptime)
        e.add_field(name='RAM Usage', value=ram)
        e.add_field(name='Guilds' if guild_count > 1 else 'Guild', value=f'{guild_count}')
        e.add_field(name='Cached Users' if guild_count > 1 else ' Cached User', value=f'{user_count}')
        e.add_field(name='Cogs', value=cogs)

        await ctx.send(embed=e)

    @commands.command(name='rungc', hidden=True)
    @commands.is_owner()
    async def run_gc(self, ctx):
        collected = gc.collect()
        await ctx.send(f'collected {collected} objects')

    @commands.command(name='ping', aliases=['latency'], hidden=True)
    @commands.is_owner()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {self.bot.latency * 1000} ms')

    @commands.command(name='listemoji', aliases=['listemo'], hidden=True)
    @commands.is_owner()
    async def list_emo(self, ctx):
        emos = '\n'.join(f'{e.name} {e.id}' for e in ctx.guild.emojis)
        await ctx.send(emos)

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        '''Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner'''

        if not cog.startswith('cogs.'):
            cog = f'cogs.{cog}'

        if not cog in EXTENSIONS:
            await ctx.send('**`COG NOT FOUND`**')
            return

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        '''Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner'''

        if not cog.startswith('cogs.'):
            cog = f'cogs.{cog}'

        if cog == 'cogs.owner':
            await ctx.send('**`NOT ALLOWED`**')
            return

        if not cog in EXTENSIONS:
            await ctx.send('**`COG NOT FOUND`**')
            return

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

def setup(bot):
    bot.add_cog(Owner(bot))