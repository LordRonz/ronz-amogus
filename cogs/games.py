from discord.ext import commands
from utils.add_reaction import flushed
from utils.triv import get_trivia, Triv
import discord
from asyncio import TimeoutError

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='trivia', aliases=['triv'])
    @commands.cooldown(1, 6.9, commands.BucketType.user)
    @commands.guild_only()
    async def trivia(self, ctx):
        '''Answer some trivia!'''

        async with ctx.typing():
            await flushed(ctx.message)
            triv: Triv = await get_trivia()

        if not triv:
            await ctx.reply('`**ERROR**: Something went wrong`')
            return

        author = ctx.author.name + "'s trivia question"
        author_icon = str(ctx.author.avatar_url)
        embed = await self.triv_embed(triv, author, author_icon)
        await ctx.reply(embed=embed)

        def check_reply(m):
            return m.author == ctx.message.author and m.channel == ctx.channel
        
        try:
            msg = await self.bot.wait_for('message', timeout=triv.time, check=check_reply)
        except TimeoutError:
            await ctx.reply('You did not answer in time, what the fuck??')
            return

        if len(ans:=msg.content.lower()) != 1 or not 0 <= (i:=ord(ans) - 97) < 4:
            await ctx.reply(f'no dumbass, the correct answer was `{triv.correct_answer}`')
            return

        if triv.answers[i] == triv.correct_answer:
            await ctx.reply('You got that answer correct genius')

        else:
            await ctx.reply(f'no dumbass, the correct answer was `{triv.correct_answer}`')

    @staticmethod
    async def triv_embed(triv: Triv, author: str, author_icon: str):
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name=author, icon_url=author_icon)
        desc = f'''**{triv.question}**

*You have {triv.time} seconds to answer with the correct letter.*

A) *{triv.answers[0]}*
B) *{triv.answers[1]}*
C) *{triv.answers[2]}*
D) *{triv.answers[3]}*
'''
        embed.description = desc
        embed.add_field(name='Difficulty', value=f'`{triv.difficulty}`', inline=True)
        embed.add_field(name='Category', value=f'`{triv.category}`', inline=True)
        embed.set_footer(text='Use the letter of the correct answer')
        return embed


def setup(bot):
    bot.add_cog(Games(bot))
