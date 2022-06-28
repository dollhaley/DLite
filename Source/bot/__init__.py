import discord
import os

from discord.ext.commands import CommandOnCooldown

from dotenv import load_dotenv, find_dotenv
from mega import Mega
from redvid import Downloader
from yt_dlp import YoutubeDL
from discord.ext.commands import Bot

load_dotenv(find_dotenv())

env = os.environ

mega = Mega().login(env['MAIL'], env['PWD'])
reddit = Downloader(max_q = True, log = False, max_d = 600)
ytmp4 = YoutubeDL({"format" : "best", "outtmpl" : "%(title)s.mp4", "quiet" : True})
ytmp3 = YoutubeDL({"format" : "best", "outtmpl" : "%(title)s.mp3", "quiet" : True})


class DLite(Bot):
    def __init__(self):
        self.mega = mega
        self.reddit = reddit
        self.mp4 = ytmp4
        self.mp3 = ytmp3

        super().__init__(
            command_prefix = "dl>",
            help_command = None,
            intents = discord.Intents.all()
            )

    def setup(self):
        for f in os.listdir("./Source/cog"):
            if f.endswith(".py"):
                self.load_extension(f"Source.cog.{f[:-3]}")
    

    def run(self):
        token = env['TOKEN']

        self.setup()

        super().run(token)


    async def on_ready(self):
        guild_status = f"{len(self.guilds)} server" if len(self.guilds) == 1 else f"{len(self.guilds)} servers"

        await self.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = guild_status))
        print("Active")

    async def on_guild_join(self, guild):
        guild_status = f"{len(self.guilds)} server" if len(self.guilds) == 1 else f"{len(self.guilds)} servers"

        await self.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = guild_status))
        
       
    async def on_command_error(self, ctx, exception):
        if isinstance(exception, CommandOnCooldown):
            await ctx.reply("You are being rate limited. Use the command again in `{}` seconds.".format(round(exception.retry_after)))

    async def on_application_command_error(self, ctx, exception):
        if isinstance(exception, CommandOnCooldown):
            await ctx.respond("You are being rate limited. Use the command again in `{}` seconds.".format(round(exception.retry_after)))

            
bot = DLite()
