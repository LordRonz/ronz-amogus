import os
import discord
from discord.ext import commands
from read_env import read_env
from keep_alive import keep_alive

read_env()

TOKEN = os.getenv('TOKEN')

extensions = [
    'cogs.text',
    'cogs.memer',
    'cogs.ascii_art',
    'cogs.nsfw',
    'cogs.animal',
    'cogs.voice',
]

bot = commands.Bot(
        command_prefix='69',
        description='SUS\nAMOGUS',
        activity=discord.Game(name="ur mum"),
    )

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

@bot.check
def no_pm(ctx):
    return not ctx.guild is None

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

keep_alive()
bot.run(TOKEN, bot=True, reconnect=True)