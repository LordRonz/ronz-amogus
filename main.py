def main():
    import os
    import discord
    from discord.ext import commands, tasks
    from read_env import read_env
    from keep_alive import keep_alive
    from utils.custom_help import MyHelpCommand
    from itertools import cycle
    import logging
    import gc

    read_env()

    TOKEN = os.getenv('TOKEN')

    extensions = (
        'cogs.text',
        'cogs.memer',
        'cogs.ascii_art',
        'cogs.nsfw',
        'cogs.animal',
        'cogs.voice',
        'cogs.error_handler',
        'cogs.owner',
    )

    logging.basicConfig()
    log = logging.getLogger('ronz-AMOGUS')
    log.setLevel(logging.INFO)

    activities = cycle((
        'ur mum',
        'ur sis',
        'ur aunt',
        'ur stepsis',
        'ur dad\'s wife',
    ))

    CMD_PREFIX = '69'
    DOCS_SITE = 'ronz-amogus.vercel.app'

    bot = commands.Bot(
            command_prefix=CMD_PREFIX,
            description='SUS\nAMOGUS',
            case_insensitive=True,
            help_command=MyHelpCommand(),
        )

    @bot.check
    async def no_pm(ctx):
        return not ctx.guild is None

    @bot.event
    async def on_ready():
        print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
        print(f'Cogs loaded: \n{bot.cogs.keys()}')

        change_presence.start()
        garbage_collector.start()

    @tasks.loop(hours=12)
    async def garbage_collector():
        log.info('running garbage collection...')
        collected = gc.collect()
        log.info(f'collected {collected} objects')

    @tasks.loop(minutes=30)
    async def change_presence():
        await bot.change_presence(activity=discord.Game(f'{next(activities)} | {CMD_PREFIX}help | {DOCS_SITE}'))

    for extension in extensions:
            bot.load_extension(extension)

    keep_alive()
    bot.run(TOKEN, bot=True, reconnect=True)

if __name__ == '__main__':
    main()