from discord.ext import commands
from utils.hentai_handler import random_hentai, nhentai_update
from utils.r34_handler import get_r34
from utils.add_reaction import flushed
import discord

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(name='hentai')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def hentai(self, ctx, id :str=''):
        '''Fetch random hentai from nhentai'''

        await flushed(ctx.message)
        if id and (not id.isnumeric() or len(id) > 13):
            id = None
        title, url, img_url = await random_hentai(int(id) if id else None)
        embed = discord.Embed(title=title, url=url, color=0xff0000)
        embed.set_image(url=img_url)
        message = await ctx.send(embed=embed)
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

    @commands.command(name='r34')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.guild_only()
    async def rule34(self, ctx, id=None):
        '''Fetch random pic from r/rule34'''

        await flushed(ctx.message)
        r34 = await get_r34()
        embed = discord.Embed(title=r34['title'], url=r34['permalink'], color=0xff0000)
        embed.set_image(url=r34['img'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Nsfw(bot))