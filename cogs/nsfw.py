from discord.ext import commands
from utils.hentai_handler import random_hentai
from utils.Hentai import Format
from utils.add_reaction import flushed
from utils.nekoslife import Nekoslife
from utils.nekosfun import Nekosfun
from utils.sauce_handler import get_sauce
from utils.reddit_handler import get_agw, get_gw, get_r34
import discord
import asyncio

def truncate(x: str, n: int):
    if len(x) < n:
        return x
    return x[0 : n - 4] + '...'

class Nsfw(commands.Cog):
    NH_REACTMOJI = ('⏪', '⬅️', '➡️', '⏩', '✅')
    SAUCE_REACTMOJI = ('⬅️', '➡️', '✅')

    def __init__(self, bot):
        self.bot = bot
        self.__reading_nhentai = set()
        self.__saucing = set()
        self.nekoslife = Nekoslife()
        self.nekosfun = Nekosfun()
        self.__nsfw_embed = discord.Embed(title='NSFW channel required!', description='Use NSFW commands in a NSFW marked channel (look in channel settings)', color=0xff0000)
        self.__nsfw_embed.set_image(url='https://imgur.com/oe4iK5i.gif')

    async def nsfw_check(self, ctx):
        if ctx.channel and ctx.channel.is_nsfw():
            return True

        if ctx.channel:
            await ctx.send(embed=self.__nsfw_embed)

        return False

    @commands.command(name='nhentai')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def nhentai(self, ctx, id :str=''):
        '''Fetch random hentai from nhentai'''

        if not await self.nsfw_check(ctx):
            return

        if (guild_id := f'{ctx.guild.id}') in self.__reading_nhentai:
            await ctx.send('This server is still reading a doujin!')
            return

        async with ctx.typing():
            await flushed(ctx.message)
            if id and (not id.isnumeric() or len(id) > 13):
                id = None
            nh = await random_hentai(int(id) if id else None)

            if not nh:
                await ctx.send('Hentai not found')
                return

        self.__reading_nhentai.add(guild_id)

        max_page = len(nh.image_urls)
        first_run = True
        num = 1
        while True:
            if first_run:
                embed = await self.nh_embed(nh, num, max_page)

                first_run = False
                msg = await ctx.send(embed=embed)

                if max_page == 1 and num == 1:
                    self.__reading_nhentai.discard(guild_id)
                    return

                for react in self.NH_REACTMOJI:
                    await msg.add_reaction(react)
            
            def check_react(reaction, user):
                if reaction.message.id != msg.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in self.NH_REACTMOJI:
                    return False
                return True

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.69, check=check_react)
            except asyncio.TimeoutError:
                self.__reading_nhentai.discard(guild_id)
                return

            if user != ctx.message.author:
                pass

            elif '⬅️' in (emoji := str(reaction.emoji)) and num > 1:
                num -= 1
                embed = await self.nh_embed(nh, num, max_page)

                await msg.edit(embed=embed)

            elif '➡️' in emoji and num < max_page:
                num += 1
                embed = await self.nh_embed(nh, num, max_page)

                await msg.edit(embed=embed)

            elif '⏪' in emoji and num > 1:
                num = 1
                embed = await self.nh_embed(nh, num, max_page)

                await msg.edit(embed=embed)

            elif '⏩' in emoji and num < max_page:
                num = max_page
                embed = await self.nh_embed(nh, num, max_page)

                await msg.edit(embed=embed)

            elif '✅' in emoji:
                self.__reading_nhentai.discard(guild_id)
                return
        self.__reading_nhentai.discard(guild_id)

    @commands.command(name='r34', aliases=['rule34'])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def rule34(self, ctx):
        '''Fetch random pic from r/rule34'''

        if not await self.nsfw_check(ctx):
            return

        async with ctx.typing():
            await flushed(ctx.message)
            r34 = await get_r34()
            embed = discord.Embed(title=r34.title, url=r34.permalink, color=0xff0000)
            embed.set_image(url=r34.img)
            await ctx.send(embed=embed)

    @commands.command(name='hentaigif')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def hentaigif(self, ctx):
        '''Fetch random hentai gif'''

        if not await self.nsfw_check(ctx):
            return

        async with ctx.typing():
            await flushed(ctx.message)
            hentai_gif = await self.nekoslife.get('Random_hentai_gif')
            await ctx.send(hentai_gif)
    
    @commands.command(name='hentai')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def hentai(self, ctx):
        '''Fetch random hentai'''

        if not await self.nsfw_check(ctx):
            return

        async with ctx.typing():
            await flushed(ctx.message)
            hentai = await self.nekoslife.get('hentai')
            await ctx.send(hentai)

    @commands.command(name='4k')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def four_k(self, ctx):
        '''Fetch random 4k pic ( ͡° ͜ʖ ͡°)'''

        if not await self.nsfw_check(ctx):
            return

        async with ctx.typing():
            await flushed(ctx.message)
            _4k = await self.nekosfun.get('4k')
            await ctx.send(_4k)

    @commands.command(name='agw', aliases=['asiansgonewild'])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def agw(self, ctx):
        '''Fetch random ( ͡° ͜ʖ ͡°) from r/asiansgonewild'''

        if not await self.nsfw_check(ctx):
            return

        async with ctx.typing():
            await flushed(ctx.message)
            agw = await get_agw()
            embed = discord.Embed(title=agw.title, url=agw.permalink, color=0xff0000)
            embed.set_image(url=agw.img)
            await ctx.send(embed=embed)

    @commands.command(name='gw', aliases=['gonewild'])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def gw(self, ctx):
        '''Fetch random ( ͡° ͜ʖ ͡°) from r/gonewild'''

        if not await self.nsfw_check(ctx):
            return

        async with ctx.typing():
            await flushed(ctx.message)
            gw = await get_gw()
            embed = discord.Embed(title=gw.title, url=gw.permalink, color=0xff0000)
            embed.set_image(url=gw.img)
            await ctx.send(embed=embed)

    @commands.command(name='sauce', aliases=['soz'])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def sauce(self, ctx, *, url=''):
        '''Usage: 69sauce <url> OR attach an image'''

        if not await self.nsfw_check(ctx):
            return

        if (guild_id := f'{ctx.guild.id}') in self.__saucing:
            await ctx.send('This server is still saucing!')
            return

        async with ctx.typing():
            await flushed(ctx.message)
            attachments = ctx.message.attachments
            if not attachments:
                if not url:
                    return await ctx.send('')
                # Remove Discord URL Escape if exists
                if url.startswith('<'):
                    if url.endswith('>'):
                        url = url[1:-1]
                    else:
                        url = url[1:]
                if url.endswith('>'):
                    url = url[:-1]
            else:
                url = attachments[0].url

            resdata = await get_sauce(url)
            if type(resdata) is dict:
                if not resdata:
                    return
                if 'message' in resdata:
                    return await ctx.send(resdata['message'])

        self.__saucing.add(guild_id)

        max_page = len(resdata)
        first_run = True
        num = 1
        while True:
            if first_run:
                data = resdata[num - 1]
                embed = await self.sauce_embed(data, num, max_page)

                first_run = False
                msg = await ctx.send(embed=embed)

                if max_page == 1 and num == 1:
                    self.__saucing.discard(guild_id)
                    return

                for react in self.SAUCE_REACTMOJI:
                    await msg.add_reaction(react)

            def check_react(reaction, user):
                if reaction.message.id != msg.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in self.SAUCE_REACTMOJI:
                    return False
                return True

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.69, check=check_react)
            except asyncio.TimeoutError:
                self.__saucing.discard(guild_id)
                return

            if user != ctx.message.author:
                pass

            elif '⬅️' in (emoji := str(reaction.emoji)) and num > 1:
                num -= 1
                data = resdata[num - 1]
                embed = await self.sauce_embed(data, num, max_page)

                await msg.edit(embed=embed)
            elif '➡️' in emoji and num < max_page:
                num += 1
                data = resdata[num - 1]
                embed = await self.sauce_embed(data, num, max_page)

                await msg.edit(embed=embed)
            elif '✅' in emoji:
                self.__saucing.discard(guild_id)
                return
        self.__saucing.discard(guild_id)

    @staticmethod
    async def sauce_embed(data: dict, num: int, max_page: int) -> discord.Embed:
        embed = discord.Embed(title=truncate(data.title, 256), color=0xff0000)
        desc = ''
        if data.urls:
            desc = '\n'.join(f'[Source]({url})' for url in data.urls)
        else:
            desc = 'Unknown Source'
        desc += f'\n> **Page {num}/{max_page}**\n'
        embed.description = desc

        embed.set_image(url=data.thumbnail)
        embed.set_footer(text=f'Similarity: {data.similarity}% | Powered by saucenao.com')
        return embed

    @staticmethod
    async def nh_embed(nh, num: int, max_page: int) -> discord.Embed:
        embed = discord.Embed(title=truncate(nh.title(Format.Pretty), 256), url=nh.url, color=0xff0000)
        desc = f'\n> **Page {num}/{max_page}**\n'
        embed.description = desc

        embed.set_image(url=nh.image_urls[num - 1])
        return embed

def setup(bot):
    bot.add_cog(Nsfw(bot))