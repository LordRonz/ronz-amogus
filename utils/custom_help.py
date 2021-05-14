from discord.ext import commands
import discord

class MyHelpCommand(commands.DefaultHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=0xff0000, description='')
        for page in self.paginator.pages:
            e.description = page
            await destination.send(embed=e)