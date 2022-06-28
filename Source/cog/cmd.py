import os
import asyncio
import discord

from discord.ext.commands import Cog, command, BucketType, cooldown, CommandOnCooldown
from discord import slash_command, Option
from discord import Embed
from discord import Color

patterns = [
    "youtu.be",
    "youtube.com/watch?",
    "twitter.com/",
    "twitter.com/i/status",
    "twitch.tv",
    '9gag.com/gag',
    "instagram.com",
    "fb.watch",
    "tiktok.com",
    "/comments/",
    "redd.it",
    "redgifs.com",
    "gfycat.com",
]

sites = [
    "`YouTube`",
    "`TikTok`",
    "`Facebook`",
    "`Twitter`",
    "`Instagram`",
    "`Reddit`",
    "`Twitch`",
    "`RedGifs`",
    "`9GAG`",
    "`Gfycat`",
]

guild = [989931549191438357]


class Commands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name = "help")
    async def help_embed(self, ctx):
        embed = Embed(
            color = Color.blurple(),
            description = f"*The prefix is `{self.bot.command_prefix}` but also supports slash commands*"
        )
        embed.set_author(name = f"{self.bot.user.name} Support")
        fields = [
            ("help", "Displays this page", False),
            ("about", "Displays a detailed info about the bot", False),
            ("save", "Downloads from given URL and file format (video or audio)", False)
        ]

        for n, v, i in fields:
            embed.add_field(name = n, value = f"<:reply:991143029073248326> {v}", inline = i)

        await ctx.reply(embed = embed)

    @slash_command(name = 'help', description = 'Displays the help page')
    async def slash_help_embed(self, ctx):
        embed = Embed(
            color = Color.blurple(),
            description = f"*The prefix is `{self.bot.command_prefix}` but also supports slash commands*"
        )
        embed.set_author(name = f"{self.bot.user.name} Support")
        fields = [
            ("help", "Displays this page", False),
            ("about", "Displays a detailed info about the bot", False),
            ("save", "Downloads from given URL and file format (video or audio)", False)
        ]

        for n, v, i in fields:
            embed.add_field(name = n, value = f"<:reply:991143029073248326> {v}", inline = i)

        await ctx.respond(embed = embed)

    @command(name = 'about')
    async def dlite_about(self, ctx):
        embed = Embed(
            color = Color.blurple()
        )
        embed.set_author(name = f"About {self.bot.user.name}")
        embed.set_thumbnail(url = self.bot.user.avatar)

        fields = [
            ("Inspired By", "DLite was inspired by the now-inactive SaveVideo Bot by `enes-tryk` and `ProfTahseen` of GitHub", False),
            ("Discord's Size Limit", "The bot uses MEGA.io to host files that exceed the limit", False),
            ("Supported Sites", ", ".join(map(str, sites)), False),
            ("Add a Star", "[Click this to go the the repository and maybe add a star](https://github.com/dollhaley/DLite)", False)
        ]

        for n, v, i in fields:
            embed.add_field(name = n, value = f'<:reply:991143029073248326> {v}', inline = i)

        await ctx.reply(embed = embed)

    @slash_command(name = 'about', description = 'Displays a detailed info about the bot')
    async def slash_dlite_about(self, ctx):
        embed = Embed(
            color = Color.blurple()
        )
        embed.set_author(name = f"About {self.bot.user.name}")
        embed.set_thumbnail(url = self.bot.user.avatar)

        fields = [
            ("Inspired By", "DLite was inspired by the now-inactive SaveVideo Bot by `enes-tryk` and `ProfTahseen` of GitHub", False),
            ("Discord's Size Limit", "The bot uses MEGA.io to host files that exceed the limit", False),
            ("Supported Sites", ", ".join(map(str, sites)), False),
            ("Add a Star", "[Click this to go the the repository and maybe add a star](https://github.com/dollhaley/DLite)", False)
        ]

        for n, v, i in fields:
            embed.add_field(name = n, value = f'<:reply:991143029073248326> {v}', inline = i)

        await ctx.respond(embed = embed)

    @command(name = 'save')
    @cooldown(1, 30, BucketType.user)
    async def video_save(self, ctx, url = None, *, mode = "video"):
        vidformat = mode.lower()
        if not url:
            await ctx.reply("Video URL not found.")

        elif vidformat not in ['video', 'audio']:
            await ctx.reply("Video format not supported. Choose one between (video, audio)")

        else:
            ydl = self.bot.mp4 if vidformat == 'video' else self.bot.mp3

            if any(pattern in url for pattern in patterns) == False:
                await ctx.reply(f"Video platform is not supported. See `{self.bot.command_prefix}about` for supported sites.")

            else:
                if any(p in url for p in ['/comments/', 'redd.it']) == True:
                    if vidformat == 'audio':
                        await ctx.reply("Cannot convert video from Reddit as audio.")

                    else:              
                        self.bot.reddit.url = url.strip()
                        self.bot.reddit.download()

                else:
                    data = ydl.extract_info(url = url.strip(), download = False)

                    str_duration = data['duration_string']

                    duration_count = len(str_duration)

                    if duration_count > 2:
                        if duration_count == 5:
                            mins = int(str_duration[:2])

                        elif duration_count == 4:
                            mins = int(str_duration[0])

                        secs = int(str_duration[-2:-1])

                        total = (mins * 60) + secs

                    else:
                        total = int(str_duration)

                    maxlim = 1200
                    if total > maxlim:
                        return await ctx.reply(f"Video duration is longer than `{round(maxlim / 60)}` minutes.")

                    ydl.download([url.strip()])

                for file in os.listdir():
                    if file.endswith("mp3") or file.endswith('mp4'):
                        bytecount = os.path.getsize(file)

                        if bytecount > 7500000:
                            try:
                                upload = self.bot.mega.upload(file)
                                link = self.bot.mega.get_upload_link(upload)

                            except:
                                await ctx.reply("An error has ocurred.")

                            else:
                                embed = Embed(
                                    color = Color.blurple(),
                                    title = "Uploaded",
                                    description = f'Request has finished uploading.\n[Click this to check it]({link})'
                                )

                                await ctx.reply(embed = embed, delete_after = 30.0)
                                os.remove(file)

                                await asyncio.sleep(1800.0)
                                self.bot.mega.destroy_url(link)

                        else:
                            content = "Download has finished."

                            await ctx.reply(content = content, file = discord.File(file), delete_after = 30.0)
                        
                        if os.path.isdir('redvid_temp'):
                            os.rmdir('redvid_temp')

                        if os.path.isfile(file):
                            os.remove(file)

    @slash_command(name = 'save', description = "Downloads from given URL with given format. Defaults to video.")
    @cooldown(1, 30, BucketType.user)
    async def video_dl(self, ctx, url: Option(str, "Video URL"), vidformat: Option(str, "Video format", choices = ['video', 'audio'], default = 'video')):
            ydl = self.bot.mp4 if vidformat == 'video' else self.bot.mp3

            if any(pattern in url for pattern in patterns) == False:
                await ctx.respond(f"Video platform is not supported. See `{self.bot.command_prefix}about` for supported sites.")

            else:
                if any(p in url for p in ['/comments/', 'redd.it']) == True:
                    if vidformat == 'audio':
                        await ctx.respond("Cannot convert video from Reddit as audio.")

                    else:              
                        self.bot.reddit.url = url.strip()
                        self.bot.reddit.download()

                else:
                    data = ydl.extract_info(url = url.strip(), download = False)

                    str_duration = data['duration_string']

                    duration_count = len(str_duration)

                    if duration_count > 2:
                        if duration_count == 5:
                            mins = int(str_duration[:2])

                        elif duration_count == 4:
                            mins = int(str_duration[0])

                        secs = int(str_duration[-2:-1])

                        total = (mins * 60) + secs

                    else:
                        total = int(str_duration)

                    maxlim = 1200
                    if total > maxlim:
                        return await ctx.respond(f"Video duration is longer than `{round(maxlim / 60)}` minutes.")

                    ydl.download([url.strip()])

                for file in os.listdir():
                    if file.endswith("mp3") or file.endswith('mp4'):
                        bytecount = os.path.getsize(file)

                        if bytecount > 7500000:
                            try:
                                upload = self.bot.mega.upload(file)
                                link = self.bot.mega.get_upload_link(upload)

                            except:
                                await ctx.respond("An error has ocurred.")

                            else:
                                embed = Embed(
                                    color = Color.blurple(),
                                    title = "Uploaded",
                                    description = f'Request has finished uploading.\n[Click this to check it]({link})'
                                )

                                await ctx.respond(embed = embed, delete_after = 30.0)
                                os.remove(file)

                                await asyncio.sleep(1800.0)
                                self.bot.mega.destroy_url(link)

                        else:
                            content = "Download has finished."

                            await ctx.respond(content = content, file = discord.File(file), delete_after = 30.0)
                        
                        if os.path.isdir('redvid_temp'):
                            os.rmdir('redvid_temp')

                        if os.path.isfile(file):
                            os.remove(file)


def setup(bot):
    bot.add_cog(Commands(bot))