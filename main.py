import os
import discord
import requests
from discord.ext import commands
from read_env import read_env
from random import choice
from keep_alive import keep_alive
from add_reaction import flushed
from meme_handler import get_meme
from hentai_handler import random_hentai, check_valid_hentai

read_env()

TOKEN = os.getenv('TOKEN')
AMOGUS_COUNT = 7
GOOBA_URL = os.getenv('GOOBA')

amoguses = []
for i in range(AMOGUS_COUNT):
    with open(f'./amoguses/amogus{i}.txt', 'r') as f:
        amoguses.append(f.read())

with open(f'./random_txt/nice_cock.txt', 'r') as f:
    nice_cock = f.read()

with open(f'./random_txt/zukowei.txt', 'r') as f:
    zukowei = f.read()

with open(f'./profanities/profanities.txt', 'r') as f:
    profanities = f.readlines()

gooba_lyrics = requests.get(GOOBA_URL).text

bot = commands.Bot(
        command_prefix='69',
        description='SUS\nAMOGUS',
        activity=discord.Game(name="ur mum"),
    )

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='amogus', help='When the impostor is sus 😳')
@commands.cooldown(1, 3, commands.BucketType.guild)
async def amogus(ctx):
    await flushed(ctx.message)
    await ctx.send(choice(amoguses))

@bot.command(name='swear', help='Fuck')
@commands.cooldown(1, 3, commands.BucketType.guild)
async def swear(ctx):
    await flushed(ctx.message)
    await ctx.send(choice(profanities))

@bot.command(name='gooba', help='Gooba Lyrics')
@commands.cooldown(1, 3, commands.BucketType.guild)
async def gooba(ctx):
    await flushed(ctx.message)
    await ctx.send(gooba_lyrics)

@bot.command(name='cock', help='Nice COCK')
@commands.cooldown(1, 3, commands.BucketType.guild)
async def cock(ctx):
    await flushed(ctx.message)
    await ctx.send(nice_cock)

@bot.command(name='yntkts', help='YO NDAK TAU KOK TANYA SAYA')
@commands.cooldown(1, 3, commands.BucketType.guild)
async def yntkts(ctx):
    await flushed(ctx.message)
    await ctx.send(zukowei)

@bot.command(name='meme', help='Yes, memes')
@commands.cooldown(1, 3, commands.BucketType.guild)
async def meme(ctx):
    await flushed(ctx.message)
    title, permalink, url = await get_meme()
    embed = discord.Embed(title=title, url=permalink, color=0xff0000)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user or user.bot:
        return
    if reaction.message.author != bot.user:
        return
    if reaction.emoji != '➡️' and reaction.emoji != '⬅️':
        return
    message = reaction.message
    if not message.embeds:
        return
    embed = message.embeds[0]
    if not embed.url.startswith('https://nhentai.net/g'):
        return
    new_embed = await check_valid_hentai(embed, reaction.emoji=='➡️')
    if new_embed:
        await message.edit(embed=new_embed)

@bot.command(name='hentai', help='Warning: NSFW')
@commands.cooldown(1, 30, commands.BucketType.guild)
async def hentai(ctx, id=None):
    await flushed(ctx.message)
    if id and not id.isnumeric():
        id = None
    title, url, img_url = await random_hentai(int(id) if id else None)
    embed = discord.Embed(title=title, url=url, color=0xff0000)
    embed.set_image(url=img_url)
    message = await ctx.send(embed=embed)
    await message.add_reaction('⬅️')
    await message.add_reaction('➡️')

@bot.listen('on_message')
async def sus(message):
    if message.author == bot.user or message.author.bot:
        return
    if 'sus' in message.content.lower():
        await flushed(message)
        await message.channel.send('**A M O G U S**')

keep_alive()
bot.run(TOKEN)