import asyncio

import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

del ytdl_format_options

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1.0):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['connect'])
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.guild_only()
    async def join(self, ctx):
        '''Joins a voice channel'''
        if (ctx.voice_client is None) or (ctx.voice_client and not ctx.voice_client.is_playing()):
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('You are not connected to a voice channel.')


    @commands.command(aliases=['p'])
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.guild_only()
    async def play(self, ctx, *, url):
        '''Streams from a url'''

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.guild_only()
    async def volume(self, ctx, vol: int):
        '''Changes the player's volume'''

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        if not 0 < vol < 201:
            return await ctx.send('Please enter a value between 1 and 200.')

        if vc.source:
            vc.source.volume = vol / 100

        await ctx.send(f'**`{ctx.author}`**: Set the volume to **{vol}%**')

    @commands.command(aliases=['dc', 'leave'])
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.guild_only()
    async def stop(self, ctx):
        '''Stops and disconnects the bot from voice'''

        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('You are not connected to a voice channel.')
                raise commands.CommandError('Author not connected to a voice channel.')
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_state = member.guild.voice_client
        ''' Checking if the bot is connected to a channel and if there is only 1 member connected to it (the bot itself)'''

        if voice_state is not None and len(voice_state.channel.members) == 1:
            await voice_state.disconnect()

def setup(bot):
    bot.add_cog(Music(bot))