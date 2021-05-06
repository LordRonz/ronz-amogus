import os
import discord
import requests
from discord.ext import commands
from read_env import read_env
from random import choice
from keep_alive import keep_alive

read_env()

TOKEN = os.getenv('TOKEN')
AMOGUS_COUNT = 7
GOOBA_URL = os.getenv('GOOBA')

amoguses = []
for i in range(AMOGUS_COUNT):
    with open(f'./amoguses/amogus{i}.txt', 'r') as f:
        amoguses.append(f.read())

with open(f'./nice_cock.txt', 'r') as f:
    nice_cock = f.read()

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
@commands.cooldown(1, 3, commands.BucketType.user)
async def amogus(ctx):
    await ctx.send(choice(amoguses))

@bot.command(name='swear', help='Fuck')
@commands.cooldown(1, 3, commands.BucketType.user)
async def swear(ctx):
    await ctx.send(choice(profanities))

@bot.command(name='gooba', help='Gooba Lyrics')
@commands.cooldown(1, 3, commands.BucketType.user)
async def gooba(ctx):
    await ctx.send(gooba_lyrics)

@bot.command(name='cock', help='Nice COCK')
@commands.cooldown(1, 3, commands.BucketType.user)
async def cock(ctx):
    await ctx.send(nice_cock)

@bot.listen('on_message')
async def sus(message):
    if message.author == bot.user or message.author.bot:
        return
    if 'sus' in message.content.lower():
        await message.channel.send('**A M O G U S**')

keep_alive()
bot.run(TOKEN)