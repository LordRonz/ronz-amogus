from discord.ext import commands
import discord

class MyHelpCommand(commands.DefaultHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(
            title=f'{self.context.bot.user.display_name} Command List',
            color=0xff0000,
            description='',
            url='https://ronz-amogus.vercel.app/',
        )
        source_code = '\n[More Details](https://ronz-amogus.vercel.app/)'
        for page in self.paginator.pages:
            e.description = page
            e.description += source_code
            await destination.send(embed=e)