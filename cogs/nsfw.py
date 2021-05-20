from discord.ext import commands
from utils.hentai_handler import random_hentai, nhentai_update
from utils.r34_handler import get_r34
from utils.add_reaction import flushed
from utils.nekoslife_handler import (
    get_hentai,
    get_hentai_gif,
)
from utils.sauce_handler import get_sauce
from utils.reddit_handler import get_agw, get_gw
import discord
import asyncio

def truncate(x: str, n: int):
    if len(x) < n:
        return x
    return x[0 : n - 4] + "..."

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.channel and ctx.channel.is_nsfw():
            return True
        
        if ctx.channel:
            await ctx.send('NSFW channel required!')
        
        return False

    @commands.Cog.listener('on_reaction_add')
    async def nhentai_nav(self, reaction, user):
        if user == self.bot.user or user.bot:
            return
        if reaction.message.author != self.bot.user or not reaction.message.guild:
            return
        if reaction.emoji != '➡️' and reaction.emoji != '⬅️':
            return
        message = reaction.message
        if not message.embeds:
            return
        embed = message.embeds[0]
        if not embed.url.startswith('https://nhentai.net/g'):
            return
        new_embed = await nhentai_update(embed, reaction.emoji=='➡️')
        if new_embed:
            await message.edit(embed=new_embed)

    @commands.command(name='nhentai')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def nhentai(self, ctx, id :str=''):
        '''Fetch random hentai from nhentai'''

        async with ctx.typing():
            await flushed(ctx.message)
            if id and (not id.isnumeric() or len(id) > 13):
                id = None
            nh = await random_hentai(int(id) if id else None)

            if not nh:
                await ctx.send('Hentai not found')
                return

            embed = discord.Embed(title=nh['title'], url=nh['url'], color=0xff0000)
            embed.set_image(url=nh['img_url'])
            message = await ctx.send(embed=embed)
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')

    @commands.command(name='r34', aliases=['rule34'])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def rule34(self, ctx, id=None):
        '''Fetch random pic from r/rule34'''

        async with ctx.typing():
            await flushed(ctx.message)
            r34 = await get_r34()
            embed = discord.Embed(title=r34['title'], url=r34['permalink'], color=0xff0000)
            embed.set_image(url=r34['img'])
            await ctx.send(embed=embed)

    @commands.command(name='hentaigif')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def hentaigif(self, ctx, id=None):
        '''Fetch random hentai gif'''

        async with ctx.typing():
            await flushed(ctx.message)
            hentai_gif = await get_hentai_gif()
            await ctx.send(hentai_gif)
    
    @commands.command(name='hentai')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def hentai(self, ctx, id=None):
        '''Fetch random hentai'''

        async with ctx.typing():
            await flushed(ctx.message)
            hentai = await get_hentai()
            await ctx.send(hentai)

    @commands.command(name='agw', aliases=['asiansgonewild'])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def agw(self, ctx, id=None):
        '''Fetch random ( ͡° ͜ʖ ͡°) from r/asiansgonewild'''

        async with ctx.typing():
            await flushed(ctx.message)
            agw = await get_agw()
            embed = discord.Embed(title=agw['title'], url=agw['permalink'], color=0xff0000)
            embed.set_image(url=agw['img'])
            await ctx.send(embed=embed)

    @commands.command(name='gw', aliases=['gonewild'])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def gw(self, ctx, id=None):
        '''Fetch random ( ͡° ͜ʖ ͡°) from r/gonewild'''

        async with ctx.typing():
            await flushed(ctx.message)
            gw = await get_gw()
            embed = discord.Embed(title=gw['title'], url=gw['permalink'], color=0xff0000)
            embed.set_image(url=gw['img'])
            await ctx.send(embed=embed)

    @commands.command(name='sauce', aliases=['soz'])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def sauce(self, ctx, *, url=""):
        '''Usage: 69sauce <url> OR attach an image'''

        async with ctx.typing():
            await flushed(ctx.message)
            attachments = ctx.message.attachments
            if not attachments:
                if not url:
                    return await ctx.send('')
                # Remove Discord URL Escape if exists
                if url.startswith("<"):
                    if url.endswith(">"):
                        url = url[1:-1]
                    else:
                        url = url[1:]
                if url.endswith(">"):
                    url = url[:-1]
            else:
                url = attachments[0].url

            resdata = await get_sauce(url)
            if type(resdata) is dict:
                if not resdata:
                    return
                if 'message' in resdata:
                    return await ctx.send(resdata['message'])

        max_page = len(resdata)
        first_run = True
        num = 1
        while True:
            if first_run:
                data = resdata[num - 1]
                embed = await self.sauce_embed(data)

                first_run = False
                msg = await ctx.send(embed=embed)

            reactmoji = []
            if max_page == 1 and num == 1:
                return
            if num == 1:
                reactmoji.append('⏩')
            elif num == max_page:
                reactmoji.append('⏪')
            elif num > 1 and num < max_page:
                reactmoji.extend(['⏪', '⏩'])
            reactmoji.append('✅')

            for react in reactmoji:
                await msg.add_reaction(react)

            def check_react(reaction, user):
                if reaction.message.id != msg.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in reactmoji:
                    return False
                return True

            try:
                res, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check_react)
            except asyncio.TimeoutError:
                return await msg.clear_reactions()

            if user != ctx.message.author:
                pass
            elif "⏪" in str(res.emoji):
                num = num - 1
                data = resdata[num - 1]
                embed = await self.sauce_embed(data)

                await msg.clear_reactions()
                await msg.edit(embed=embed)
            elif "⏩" in str(res.emoji):
                num = num + 1
                data = resdata[num - 1]
                embed = await self.sauce_embed(data)

                await msg.clear_reactions()
                await msg.edit(embed=embed)
            elif "✅" in str(res.emoji):
                await ctx.message.delete()
                return await msg.delete()

    async def sauce_embed(self, data: dict) -> discord.Embed:
        embed = discord.Embed(title=truncate(data.title, 256), color=0xff0000)
        desc = ''
        if data.urls:
            desc = '\n'.join(f'[Source]({url})' for url in data.urls)
        else:
            desc = 'Unknown Source'
        embed.description = desc

        embed.set_image(url=data.thumbnail)
        embed.set_footer(text=f'Similarity: {data.similarity}% | Powered by saucenao.com')
        return embed

def setup(bot):
    bot.add_cog(Nsfw(bot))