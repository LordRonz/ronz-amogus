from discord.ext import commands
from utils.bible import get_bible, Bible
from utils.quran import get_quran, Quran
from typing import Optional
from random import randint
import discord

class Holy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='bible', aliases=['bib'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()
    async def bible(self, ctx: commands.Context, *, msg: str = ''):
        '''Read the bible!'''

        parse = msg.lower().split()

        verse = '+'.join(parse)

        if len(parse) > 100:
            await ctx.send('Woah my dude, what kind of verse is that?')
            return

        bible: Bible = await get_bible(verse)

        if not bible:
            await ctx.send('Not found')
            return

        embed = discord.Embed(title=bible.reference, description=bible.text, color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name='quran', aliases=['koran'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()
    async def quran(self, ctx: commands.Context, *, msg: str = ''):
        '''Read the Quran!'''

        parse = msg.split()

        ayah = ''.join(parse) if msg else f'{randint(1, 6236)}'

        if len(ayah) > 20:
            await ctx.send('Not a valid ayah!')
            return

        quran: Optional[Quran] = await get_quran(ayah)

        if not quran:
            await ctx.send('Not found')
            return

        embed = discord.Embed(title=f'{quran.en_name} ({quran.name}) {quran.num}:{quran.num_in_surah}', color=0x00ff00)
        embed.add_field(name='Arabic', value=quran.arab_text, inline=False)
        embed.add_field(name='English', value=quran.text, inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Holy(bot))
