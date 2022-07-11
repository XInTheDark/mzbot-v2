# bot.py
import asyncio
import datetime
import json
import os
import random
import sys
import timeit
import socket
import youtube_dl
import urllib.request
import re
import speedtest

import discord
import discord.abc
import pytz
from PyDictionary import PyDictionary
from discord.ext import commands
from discord.ext.commands.errors import *
from dotenv import load_dotenv
from requests import get

import mzhelp
import mzutils

# Setting variables
global afkdict
afkdict = {}
spam_ban = [726356086176874537]
global user
global reaction
global antinuke
global bansdict
global snipes
global esnipes
global uptime
global hardmutes
global ownerid
global istyping
global msgpings
global launch_time
global downloadSpeed

antinuke = []
bansdict = {}
snipes = {}
esnipes = {}
uptime = 0
hardmutes = []
ownerid = 926410988738183189
istyping = []
msgpings = {}
musicDict = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# TOKEN = "OTQ2NzYxODIzMzg0OTE1OTY4.YhjaqA.RjZrEx-MnlA8a42ZetXvSOnfo8g"
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
# activity = discord.Activity(type=discord.ActivityType.listening, name=f".help | {len(bot.guilds)} servers")
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='.', help_command=None, intents=intents)

# definitions
def speedTestDownload():
    wifi = speedtest.Speedtest()
    return round((wifi.download())/1048576, 2)

def speedTestUpload():
    wifi = speedtest.Speedtest()
    return round((wifi.upload())/1048576, 2)


@bot.event
async def on_ready():
    global uptime

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
    # computer_name = os.environ['USERNAME']
    embed = discord.Embed(title="**MZ Bot build succeeded**",
                          description=f"**MZ Bot started at <t:{int(launch_time.timestamp())}:f> (<t:{int(launch_time.timestamp())}:R>)**\n"
                                      f"\nHost IP: __{local_ip}__\nHost: {os.uname()}\n\nHost info: {os.environ}",
                          color=0x00ff00)
    # await channel.send(embed=embed)
    await channel.send(embed=embed)
    print("MZ Bot start-up complete")

    # init variables
    downloadSpeed = speedTestDownload()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, BotMissingPermissions):
        await ctx.send(f'`Missing Permissions!`')
    if isinstance(error, BotMissingAnyRole):
        await ctx.send(f'`Missing Roles!`')
    if isinstance(error, CommandInvokeError):
        msg = await ctx.send(f'`{error}`')
        # await asyncio.sleep(3)
        # await msg.delete()
    if isinstance(error, CommandOnCooldown):
        msg = await ctx.reply(f'`{error}`')
        await asyncio.sleep(3)
        await msg.delete()
    if isinstance(error, MissingRequiredArgument) or isinstance(error, TooManyArguments):
        await ctx.send(f'`Missing Required Arguments!`\nFor the command\'s help page, type `.help <command>`!')
    if isinstance(error, CommandNotFound):
        msg = await ctx.send(f'`Command not found!`')
        await asyncio.sleep(3)
        await msg.delete()

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.mention}! Welcome to our server! We hope you enjoy your stay :) ")


@bot.event
async def on_guild_join(guild):
    await guild.text_channels[0].send(
        "Hey! I'm MZ Bot! To view all commands, type `.help`! To check the update logs, type `.update`!")


@bot.event
async def on_message(message):
    global afkdict
    global hardmutes
    global msgpings

    if message.content.strip() == "<@946761823384915968>":
        await message.reply(
            "Hey! I'm MZ Bot! To view all commands, type `.help`! To check the update logs, type `.update`!")

    if message.author.id in hardmutes:
        await message.delete()

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
                await message.author.edit(nick=message.author.display_name.removeprefix("[AFK] "))
            except:
                None

            await asyncio.sleep(7.5)
            await welcomebackmsg.delete()

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

    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    msg = message.content
    author = message.author

    if author.id != bot.user.id:
        snipes[len(snipes)] = [author, message.channel.id, msg, round(message.created_at.timestamp()),
                               round(datetime.datetime.utcnow().timestamp())]


@bot.event
async def on_message_edit(old, new):
    oldmsg = old.content
    newmsg = new.content
    author = new.author

    if author.id != bot.user.id:
        esnipes[len(esnipes)] = [author, old.channel.id, oldmsg, newmsg, round(old.created_at.timestamp()),
                                 round(datetime.datetime.utcnow().timestamp())]


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


@bot.command(name='update', aliases=['updates', 'log', 'logs', 'announcements', 'notes'])
async def updatelog(ctx):
    message = """New Update: 14/06/2021
- MZ Bot has returned after 7 months!! 
*Note: 1. This log only shows the LATEST update notes.
2. The notes will only be updated for MAJOR updates, not small patches.*"""

    embed = discord.Embed(title="**Update Log**", description=message, color=0x00ff00)
    await ctx.reply(embed=embed)


@bot.command(name='help', aliases=['commands', 'cmds'])
async def help(ctx, cmd=None):
    response = """**List of commands**
**Public:**
- meme
- donate
- dice
- credits
- ticket
- delete (For your own ticket)
- nitro
- afk
- about
- ping
- updates
- timedif
- dmnitro
- membercount
- snipe
- editsnipe
- whois
**Requires permissions:**
- dw
- mute
- unmute
- nuke
- kick
- ban
- unban
- gg
- tips
- claimed
- won
- setproofschannel
- setclaimschannel
- spam
- dmspam
- dmspam_force
- lockall
- slowmode
- purge
- setnsfw
- timer
**Experimental features available:**
None

*Note: Other features that may exist are solely for Alpha testing and not for public usage.*

**You may use `.help <command>` for help on that command.**"""

    helpdict = mzhelp.helpcmdz
    usagedict = mzhelp.helpusage

    if cmd is None:
        embed = discord.Embed(title="Help Page", description=response, color=0x00ff00)

        msg1 = await ctx.send("Loading...")
        await asyncio.sleep(0.01)
        await ctx.reply(embed=embed)
        await msg1.delete()


    else:
        found = False
        helpd = ''
        usaged = ''
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

            msgo = await ctx.send("Loading...")
            await asyncio.sleep(0.01)
            await msgo.delete()
            msg = await ctx.reply(embed=embed)

        else:
            await ctx.reply("I cannot find that command.")


@bot.event
async def on_member_ban(guild, user):
    global antinuke
    global ownerid
    global bansdict
    guildid = guild.id
    # try:
    #     bansdict[guildid] = guild.bans()[guildid] + 1
    # except:
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
                except:
                    None

            for member in guild.members:
                try:
                    await member.kick(reason=random.choice(krlist))
                except:
                    None

            try:
                try:
                    text_channel_list = []

                    for channel in guild.text_channels:
                        text_channel_list.append(channel)

                    for channel in text_channel_list:
                        try:
                            await channel.delete()
                        except:
                            None

                except:
                    None

                finally:
                    None
            except:
                None
            finally:
                None

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
http://pornhub.com/**""")
                except:
                    newchannel = random.choice(guild.text_channels)

                try:
                    await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
                    await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
                except:
                    None


# ANTI NUKE
@bot.command(name='antinuke', aliases=['protect', 'protection', 'shield'])
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    global antinuke

    guildid = ctx.message.guild.id
    if not guildid in antinuke:
        antinuke.append(guildid)
        await ctx.reply("Antinuke is now enabled! To disable antinuke, use `.disableantinuke`.")
    else:
        await ctx.reply("Antinuke is already enabled for this server!")


@bot.command(name='disableantinuke', aliases=['disableprotect', 'disableprotection', 'offshield'])
@commands.has_permissions(administrator=True)
async def disableantinuke(ctx):
    guildid = ctx.message.guild.id
    if guildid in antinuke:
        antinuke.pop(guildid)
        await ctx.reply("Antinuke is now disabled! To enable antinuke, use `.antinuke`.")
    else:
        await ctx.reply("Antinuke is already disabled for this server!")


@bot.command(name='dw', help='Responds how a drop works.')
async def drop(ctx):
    response = """**How does a drop work?**
    -> Every drop usually lasts for a short time!
    -> The winner of the drop gets 10-30 seconds to DM the host!"""
    await ctx.send(response)

@commands.cooldown(1, 2, commands.BucketType.user)
@bot.command(name='meme', help='Generates a random meme.')
async def plsmeme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content)
    meme = discord.Embed(title=f"{data['title']}", color=discord.Color.random()).set_image(url=f"{data['url']}")

    await ctx.reply(embed=meme)


@bot.command(name='-.', help='.-.')
async def dotdashdot(ctx):
    response = ".-. .-. .-. .-. .-. .-. .-. .-. .-. .-."

    await ctx.send(response)


@bot.command(name='_.', help='._.')
async def dotdashdot2(ctx):
    response = "._. ._. ._. ._. ._. ._. ._. ._. ._. ._."

    await ctx.send(response)


@bot.command(name='donate', help='Fund our development!')
async def donate(ctx):
    response = """To donate, you may buy any gamepass from https://www.roblox.com/games/6742216868/MuzhenGamingYTs-Place#!/store :)
    Or donate some nitro to <@926410988738183189> ;)"""

    await ctx.send(response)


@bot.command(name='dice', help="""Rolls an imaginary, non-existent die.
Usage: `.dice <number of dice> <number of sides>`""")
async def rolldice(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='credits', help='Shows some surprising credits.')
async def credits(ctx):
    response = """Credits to:
    <@926410988738183189> [MuzhenGaming#5088] and NO ONE ELSE."""

    await ctx.send(response)

@commands.cooldown(1, 0.5, commands.BucketType.channel)
@bot.command(name='nitro', help='Generates a random... Nitro code?!')
async def nitrogen(ctx):
    genlist = str(open('nitrogenlist.txt', 'r').read())
    genlistsplit = genlist.split("\n")

    response = str(random.choice(genlistsplit))

    await ctx.send(response)


@bot.command(name='shutdown', help='WTF... SHUTDOWN THE BOT?!! NO!!! NO!!!')
async def shutdown(message):
    if str(message.author.id) != str(ownerid):
        print(str(message.author.id), "Tried to shutdown the bot by using .shutdown")
        await message.send("LOL Only <@926410988738183189> can shutdown the bot, get lost\n**YOU GAY**")
    else:
        await message.send("`Shutdown Executed Successfully`")
        # quit()
        await bot.close()
        print("Shutdown command executing...")
        await asyncio.sleep(1)
        await bot.logout()
        while True:
            await asyncio.sleep(0.5)
            quit()


@bot.command(name='restart', help='WTF... SHUTDOWN THE BOT?!! NO!!! NO!!!')
async def restart(message):
    if str(message.author.id) != str(ownerid):
        print(str(message.author.id), "Tried to shutdown the bot by using .shutdown")
        await message.send("LOL Only <@926410988738183189> can shutdown the bot, get lost\n**YOU GAY**")
    else:
        await message.send("`Restart Executing...`")

        os.execv(sys.executable, ['python'] + sys.argv)
        await message.send("`Restart Executed Successfully`")


@bot.command(name='mute', help='Mutes someone.')
async def mute(ctx, member: discord.Member, *, reason=None):
    if str(ctx.author.id) != str(ownerid) and not ctx.author.guild_permissions.manage_server:
        print(str(ctx.author.id), "Tried to mute", member, "by using .mute")
        await ctx.send("You don't have permissions!")
    else:
        guild = ctx.guild
        mutedrole = discord.utils.get(guild.roles, name="Muted")
        await member.add_roles(mutedrole, reason=reason)
        await ctx.send(f"`Muted User:{member} Successfully`")


@bot.command(name='unmute', help='Unmutes someone.')
async def unmute(ctx, member: discord.Member):
    if str(ctx.author.id) != str(ownerid) and not ctx.author.guild_permissions.manage_server:
        print(str(ctx.author.id), "Tried to unmute", member, "by using .unmute")
        await ctx.send("You don't have permissions!")
    else:
        mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedrole)
        await ctx.send(f"`Unmuted User: {member} Successfully`")


@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command(name='nuke', help='Nukes this channel... Yep.')
async def nuke_channel(ctx):
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


@bot.command(name='softnuke_server', help='NUKES THE SERVER!!! ARGHHHHH NO!!!!! DONT!!', aliases=['raidstep1'])
async def nuke_server_fr(ctx):
    if str(ctx.author.id) != str(ownerid):
        print(str(ctx.author.id), "Tried to soft nuke THE ENTIRE SERVER by using .softnuke_server")
        await ctx.send(
            "LOL ONLY <@926410988738183189> can nuke THE ENTIRE SERVER ||(and why would he)||, get lost noob\n**YOU FUCKING RETARD**")
    else:
        async def nuke_channel_2(txt):
            if str(txt.author.id) != str(ownerid):
                print(str(txt.author.id), "Tried to nuke channel:", txt.channel, "by using .nuke")
                await txt.send("LOL ONLY <@926410988738183189> can nuke this channel, get lost noob\n**YOU GAY**")
            else:
                text_channel_list = []
                for channel in ctx.guild.text_channels:
                    text_channel_list.append(channel)

                try:
                    for channel in text_channel_list:
                        await channel.delete()
                except:
                    None

        await nuke_channel_2(ctx)


@bot.command(name='hardnuke_server', help='NUKES THE SERVER!!! ARGHHHHH NO!!!!! DONT!! PLSPLSPLS',
             aliases=['raidstep2'])
async def nuke_server_fr(ctx):
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
                except:
                    None

        for member in ctx.guild.members:
            if member.id != ownerid:
                try:
                    await member.kick(reason=random.choice(krlist))
                except:
                    None

        try:
            try:
                text_channel_list = []

                for channel in ctx.guild.text_channels:
                    text_channel_list.append(channel)

                for channel in text_channel_list:
                    try:
                        await channel.delete()
                    except:
                        None

                for category in ctx.guild.categories:
                    try:
                        await category.delete()
                    except:
                        None

            except:
                None

            finally:
                None
        except:
            None
        finally:
            None

        for role in ctx.guild.roles:
            try:
                await role.delete()
            except:
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
http://pornhub.com/**""")
            except:
                newchannel = random.choice(ctx.guild.text_channels)

            try:
                await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
                await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
            except:
                None


# updated.

@bot.command(name='gg', help='GG, Stay!', aliases=['ggstay', 'stay'])
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


@bot.command(name='lostleave', help='Lost, leave!', aliases=['lost'])
@commands.has_permissions(administrator=True)
async def ooflost(ctx, *, server):
    embedVar = discord.Embed(title=f"We lost! Leave **{server}**",
                             description=f"""Sorry, we lost! Leave that server (**{server}**) now!**""", color=0x00ff00)

    await ctx.channel.send(embed=embedVar)
    msgid = await ctx.channel.fetch_message(ctx.message.id)
    await msgid.delete()


@bot.command(name='tips', help='Tips for MZ Giveaways')
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


@bot.command(name='won', help='Who won the giveaway?')
@commands.has_permissions(administrator=True)
async def whowon(ctx, userid, *, prize):
    claimsfile2 = open('proofchannel.txt', 'r')
    prooflines = claimsfile2.readlines()
    server_id = ctx.message.guild.id
    foundserver = False

    for i in prooflines:
        if str(server_id) in i:
            i = i.removeprefix(f"{server_id}:")
            proofschannel = f"<#{str(i)}>"
            foundserver = True
            break
    if not foundserver:
        await ctx.channel.send(
            r"Cannot find proofs channel! Try using '.setproofschannel'!\n*(Due to a recent update, the proofs channel can now be set! We strongly encourage you to set it with `.setproofschannel`.)")
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
@commands.cooldown(1, 10, commands.BucketType.guild)
@bot.command(name='ban', help='Bans a user.')
@commands.has_permissions(ban_members=True)
async def ban(self, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await self.send(f'''User: `{member}` has been banned
Reason: {reason}
- by {self.author}''')


@commands.cooldown(1, 10, commands.BucketType.guild)
@bot.command(name='unban', help='Unbans a user.')
@commands.has_permissions(ban_members=True)
async def unban(self, *, member: str):
    banned_users = await self.guild.bans()
    found = 0
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await self.guild.unban(user)
            await self.send(f"""`{user}` has been unbanned
- by {self.author}""")
            found = 1
            break
    if found == 0:
        await self.reply("Could not find that banned user!")


@commands.cooldown(1, 10, commands.BucketType.guild)
@bot.command(name='kick', help='Kicks a user.')
@commands.has_permissions(kick_members=True)
async def kick(self, *, member: discord.Member, reason=None):
    await member.kick(reason=reason)
    await self.send(f"""User `{member}` has been kicked
Reason: {reason}
- by {self.author}""")


@bot.command(name='spam', help="""Spams a certain message a certain number of times.""")
async def spam(ctx, number_of_times, *, message):
    if ctx.author.id != ownerid and not ctx.author.guild_permissions.administrator:
        await ctx.reply("Omg why are you trying to spam here?!")
    elif ctx.author in spam_ban:
        await ctx.reply("EWWWW NOOB UR BANNED FROM SPAMMING EWWWW")
    else:
        number_of_times = int(number_of_times)

        await ctx.channel.send(f"Task started by {ctx.author}...")

        await ctx.message.delete()

        for i in range(number_of_times):
            await ctx.channel.send(message)

        number_of_times2 = str(number_of_times)

        msg2 = f"""<@{ctx.author.id}>, task done!
Server: {ctx.guild.name}
Channel: {ctx.channel.name}
Message: {message}
Number of times: {number_of_times2}
"""
        dms = await ctx.author.create_dm()
        await dms.send(msg2)


@bot.command(name='dmspam', help="""Spams a certain message a certain number of times.""")
async def spam(ctx, number_of_times, user: discord.Member, *, message):
    optoutfile = open('optoutspam.txt', 'r')
    optoutlist = []
    for x in optoutfile:
        optoutlist.append(x)

    if ctx.author.id != ownerid and not ctx.author.guild_permissions.administrator:
        await ctx.channel.send("Omg who are you trying to spam?! noob")
    elif str(user.id) in optoutlist:
        await ctx.channel.send(f"Sorry, that user [{user}] has opted out of the `dmspam` command.")
    elif ctx.author in spam_ban:
        await ctx.reply("EWWWW NOOB UR BANNED FROM SPAMMING EWWWW")
    else:
        number_of_times = int(number_of_times)

        dmchannel = await user.create_dm()

        await ctx.channel.send(f"Task started by {ctx.author}...")

        for i in range(number_of_times):
            await dmchannel.send(message)

        number_of_times2 = str(number_of_times)

        await dmchannel.send(f"""The above message(s) were requested by {ctx.author}.
        Total number of messages sent: {number_of_times2}
        **NOTE: The bot is not responsible for any of the messages sent above.**""")

        msg2 = f"""<@{ctx.author.id}>, task done!
Message: {message}
Number of times: {number_of_times2}
User: {user}
Guild: {ctx.guild.name}"""

        await ctx.channel.send(msg2)


@bot.command(name='dmspam_force', help="""Spams a certain message a certain number of times... Anonymously.""")
async def spam(ctx, number_of_times, user: discord.Member, *, message):
    if ctx.author.id != ownerid and not ctx.author.guild_permissions.administrator:
        await ctx.channel.send("Omg who are you trying to spam?! noob hacker lmao, go hack ur mom instead")
    elif ctx.author in spam_ban:
        await ctx.reply("EWWWW NOOB UR BANNED FROM SPAMMING EWWWW")
    else:
        number_of_times = int(number_of_times)

        dmchannel = await user.create_dm()

        await ctx.channel.send(f"Task started by Anonymous...")

        for i in range(number_of_times):
            await dmchannel.send(message)

        number_of_times2 = str(number_of_times)

        await dmchannel.send(f"""Information:
        Total number of messages sent: {number_of_times2}
        **NOTE: The bot is not responsible for any of the messages sent above.**""")

        msg2 = f"""<@{ctx.author.id}>, task done!
Message: {message}
Number of times: {number_of_times2}
User: {user}
Guild: {ctx.guild.name}"""

        userdm = await ctx.author.create_dm()
        await userdm.send(msg2)


@bot.command(name='optout_spam', help="""Opts out of spam.""")
async def optoutspam(ctx):
    optoutlist2 = []

    optoutfile2 = open('optoutspam.txt', 'r')
    for y in optoutfile2:
        optoutlist2.append(y)
    optoutfile2.close()

    if ctx.author.id in optoutlist2:
        await ctx.channel.send(
            "You are already in the opt-out list! If you wish to opt in again, use the command `.optin_spam`!")
    else:
        optoutfile3 = open('optoutspam.txt', 'a')
        optoutfile3.write('\n')
        optoutfile3.write(str(ctx.author.id))
        await ctx.channel.send(
            "You have opted out for spam! If you wish to opt in again, use the command `.optin_spam`!")
        optoutfile3.close()


@bot.command(name='optin_spam', help="""Opts in of spam [after opting out].""")
async def optinspam(ctx):
    optoutlist3 = []

    optoutfile3 = open('optoutspam.txt', 'r')
    for y in optoutfile3:
        optoutlist3.append(y)
    optoutfile3.close()

    if str(ctx.author.id) not in optoutlist3:
        await ctx.channel.send(
            "You are already opted in for spam! If you wish to opt out, use the command `.optout_spam`!")
    else:
        a_file = open("optoutspam.txt", "r")
        lines = a_file.readlines()
        a_file.close()

        new_file = open("optoutspam.txt", "w")
        for line in lines:
            if line.strip("\n") != str(ctx.author.id):
                new_file.write(str(line))
                new_file.close()

        await ctx.channel.send(
            "You have opted in for spam! If you wish to opt out again, use the command `.optout_spam`!")


@bot.command(name='lockall', help='Lock all channels.')
async def lockall(ctx):
    if ctx.author.id != ownerid and not ctx.author.guild_permissions.administrator:
        await ctx.channel.send("Omg why are you trying to lock channels!")
    else:
        for channel in ctx.guild.text_channels:
            if channel.overwrites_for(ctx.guild.default_role).send_messages == True:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False,
                                              reason=f'User {ctx.author} used command lockall')

        await ctx.send(f"{ctx.author.mention}, Locked all channels successfully!")


@bot.command(name='slowmode', help='Sets the slowmode for a channel.')
async def setdelay(ctx, seconds: int):
    if not ctx.author.guild_permissions.manage_messages and ctx.author.id != ownerid:
        await ctx.channel.send('You are missing `Manage Messages` permissions!')
    else:
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.channel.send(f"Set the slowmode for channel: `#{ctx.channel}` to `{seconds}` seconds!")


@bot.command(name='addrole', help='Adds a role to someome.', pass_context=True)
@commands.has_permissions(administrator=True)  # This must be exactly the name of the appropriate role
async def addrole(ctx, member: discord.Member, *, rolename):
    role = discord.utils.get(ctx.guild.roles, name=rolename)
    if str(member) == "all":
        await ctx.send(f"Adding role to {len(ctx.guild.members)} members...")

        for i in ctx.guild.members:
            try:
                await i.add_roles(role)
            except AttributeError:
                await ctx.channel.send("An Error Occurred while trying to add role! Check whether that role exists!")
                errorrole = 1
                break
        await ctx.send(
            f"{ctx.author.mention}, Added role '{rolename}' to {len(ctx.guild.members)} members successfully!")

    else:
        errorrole = 0

        try:
            await member.add_roles(role)
        except AttributeError:
            await ctx.channel.send("An Error Occurred while trying to add role! Check whether that role exists!")
            errorrole = 1

        if errorrole == 0:
            await ctx.channel.send(f"Added role: {rolename} to member {member} successfully!")


@bot.command(name='setclaimschannel', help='Set Claims Channel. (Admin Only)')
async def setclaimschannel(ctx, channel):
    if channel is not None:
        try:
            channelid = channel.removeprefix('<#').removesuffix('>')
        except:
            try:
                channelid = int(channel)
            except:
                await ctx.channel.send('An error occurred! Check your syntax!')
    else:
        channelid = ctx.channel.id

    try:
        channeltest = client.get_channel(channelid)
    except:
        await ctx.channel.send('Cannot find channel! Check your command!')

    taskdone1 = False

    if not ctx.author.guild_permissions.administrator and ctx.author.id != ownerid:
        await ctx.channel.send("Omg look at who's fiddling with server settings?!")
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

                taskdone1 = True
                await ctx.channel.send(f"Successfully updated claims channel to <#{channelid}>!")
                break

        if not taskdone1:
            claimsfile.close()
            claimsfile = open('claimschannel.txt', 'a')
            claimsfile.write('\n')
            claimsfile.write(f"{str(serverid)}:{str(channelid)}")

            await ctx.channel.send(f"Successfully updated claims channel to <#{channelid}>!")

            claimsfile.close()


@bot.command(name='claimed', help='Shows who claimed.', aliases=['claim'])
async def claimed(ctx, member: discord.Member, how, *, prize):
    if not ctx.author.guild_permissions.administrator and ctx.author.id != ownerid:
        await ctx.channel.send("You're not an administrator!")
    else:
        claimsfile2 = open('claimschannel.txt', 'r')
        claimlines = claimsfile2.readlines()
        server_id = ctx.message.guild.id
        foundserver = False

        for i in claimlines:
            if str(server_id) in i:
                i = i.removeprefix(f"{server_id}:")
                claimschannel = int(i)
                foundserver = True
                break
        if not foundserver:
            await ctx.channel.send("Cannot find claims channel! Try using '.setclaimschannel'!")
        else:
            channel = bot.get_channel(int(claimschannel))
            await channel.send(f"""🎉 **Congratulations!** 🎉
{member.mention} claimed **{prize}** from **{how}**!""")
            await ctx.message.delete()
        claimsfile2.close()


@bot.command(name='setproofschannel', help='Set Proofs Channel. (Admin Only)', aliases=['setproofchannel'])
async def setproofschannel(ctx, channelid):
    if channelid is not None:
        try:
            channelid = channelid.removeprefix('<#').removesuffix('>')
        except:
            try:
                channelid = int(channelid)
            except:
                await ctx.channel.send('An error occurred! Check your syntax!ww')
    else:
        channelid = ctx.channel.id

    try:
        channeltest = client.get_channel(channelid)
    except:
        await ctx.channel.send('Cannot find channel! Check your command!')

    taskdone1 = False

    if not ctx.author.guild_permissions.administrator and ctx.author.id != ownerid:
        await ctx.channel.send("Omg look at who's fiddling with server settings?!")
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

                taskdone1 = True
                await ctx.channel.send(f"Successfully updated proofs channel to <#{channelid}>!")
                break

        if not taskdone1:
            claimsfile.close()
            claimsfile = open('proofchannel.txt', 'a')
            claimsfile.write('\n')
            claimsfile.write(f"{str(serverid)}:{str(channelid)}")

            await ctx.channel.send(f"Successfully updated proofs channel to <#{channelid}>!")

            claimsfile.close()


@bot.command(name='rename', help='Renames the channel.', aliases=['renamechannel'])
@commands.has_permissions(manage_channels=True)
async def rename(ctx, channel='', *, name):
    channel2 = None

    if channel != '':
        try:
            channelid = channel.removeprefix('<#').removesuffix('>')
            channelid = int(channelid)
        except:
            try:
                channelid = int(channel)
            except:
                await ctx.channel.send('An error occurred! Check your syntax!')
                return
    else:
        channelid = ctx.channel.id

    try:
        channel2 = bot.get_channel(channelid)
    except:
        await ctx.channel.send('Cannot find channel! Check your command!')
        return

    await channel2.edit(name=name)
    msg1 = await ctx.reply(f"Renamed #{channel2} to #{name}")
    await asyncio.sleep(5)
    await msg1.delete()
    await ctx.message.delete()


@commands.cooldown(1, 3, commands.BucketType.channel)
@bot.command(name='purge', help='{Beta} Purge messages.')
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
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
@bot.command(name='afk', help='Sets AFK.')
async def setafk(ctx, *, reason='AFK'):
    global afkdict
    afkdict[str(ctx.author.id)] = [reason, str(int(datetime.datetime.utcnow().timestamp()))]
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.mention}, I set your AFK: {reason}")
    try:
        await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
    except:
        None


@bot.command(name='about', help='Version and developer info.', aliases=['version', 'info'])
async def checkversion(ctx):
    global uptime, launch_time

    tests = 20000  # the amount of tests to conduct
    latency_list = []  # this is where the tests go
    for x in range(tests):  # this is the loop
        latency = round(bot.latency * 1000)  # this gathers the latency
        latency_list.append(latency)  # puts the latency in the list
    lavg = round(sum(latency_list) / tests)  # averages the list out

    uptime = (datetime.datetime.utcnow() - launch_time).total_seconds()

    msg1 = await ctx.send("Loading...")

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


@bot.command(name='ping', help='Check bot ping.', aliases=['ms', 'connection'])
async def ping(ctx):
    msg1 = await ctx.send("Connecting...")
    tests = 1000000  # the amount of tests to conduct
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

    if lavg < 15:
        jud1 = 'Fast'
    elif lavg >= 15 and lavg < 40:
        jud1 = 'Normal'
    else:
        jud1 = 'Slow - Bot Lagging!'

    if secs * 1000 < 120:
        jud2 = 'Fast'
    elif secs * 1000 >= 120 and secs * 1000 < 200:
        jud2 = 'Normal'
    else:
        jud2 = 'Slow - Bot Lagging!'

    await msg1.delete()

    await ctx.reply(f"""Client Ping: {lavg} ms ({jud1})
Message Latency: {int(secs * 1000)} ms ({jud2})""")


@bot.command(name='timedif', help='', aliases=['snowflake', 'timediff'])
async def timedif(ctx, id1, id2=None):
    if ctx.message.reference is not None:
        id2 = ctx.message.reference.message_id
    try:
        id1 = int(id1)
        id2 = int(id2)

    except:
        await ctx.reply("Check your message ID's! They are incorrect!")

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


@bot.command(name='removerole', help='Adds a role to someome.', pass_context=True)
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
@bot.command(name='ticket', aliases=['tickets'])
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
        return str(reaction) == '📩' and user.id != 877804981347029043

    while True:

        await bot.wait_for("reaction_add", check=check)
        await msg.remove_reaction('📩', user)

        member = user

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        file = open('tickets.txt', 'r')
        lines = file.readlines()
        file.close()

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

            file = open('tickets.txt', 'a')
            file.write(f"{user.id}")
            file.close()


@commands.cooldown(1, 5, commands.BucketType.channel)
@bot.command(name='delete', aliases=['tdelete', 'tclose'])
@commands.has_permissions(administrator=True)
async def tclose(ctx):
    #     if isinstance(ctx.channel, discord.abc.PrivateChannel):
    channelperms = ctx.channel.overwrites_for(ctx.author)
    memberoverwrite = channelperms
    if memberoverwrite == discord.PermissionOverwrite(read_messages=True,
                                                      send_messages=True) or ctx.author.guild_permissions.manage_channels:

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
        with open("tickets.txt", "r") as file_input:
            with open("tickets.txt", "w") as output:
                for line in file_input:
                    if line.strip("\n") != str(ctx.author.id):
                        output.write(line)
    else:
        await ctx.reply("This is not your ticket!")


#         await ctx.reply("Hey! This isn't a ticket!")

@bot.command(name='define', aliases=['definition', 'meaning', 'dictionary'])
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

            meaning.removesuffix("\n")
        except:
            await ctx.reply(f"`{word}` not found in dictionary!")
            return

        embed = discord.Embed(title=f'**Definition for `{word}`**', description=f"""Definition for `{word}`:
{meaning}""", color=0x00ff00)
        embed.set_footer(text="Powered by PyDictionary | Beta")

        await ctx.reply(embed=embed)


@bot.command(name='dmnitro', aliases=['massnitro', 'nitrospam'])
async def dmnitro(ctx, amount: int):
    genlist = str(open('nitrogenlist.txt', 'r').read())
    genlistsplit = genlist.split("\n")
    channel = await ctx.author.create_dm()

    for i in range(amount):
        response = str(random.choice(genlistsplit))

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

@bot.command(name='membercount', aliases=['mc', 'members'])
async def mc(ctx):
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


@bot.command(name='snipe', aliases=['sniper'])
async def snipe(ctx, pos=1):
    success1 = False
    success2 = False

    try:
        lst = snipes[sorted(snipes.keys())[-1]]
        success1 = True
    except:
        if pos == 1:
            await ctx.reply("No messages deleted yet.")
        else:
            await ctx.reply("There is no message found at that index.")

    if success1:
        if not lst[1] == ctx.channel.id:
            success2 = False
            pos1 = pos - 1
            while True:
                try:
                    lst = snipes[sorted(snipes.keys())[-1 - pos1]]
                    if lst[1] == ctx.channel.id:
                        success2 = True
                        break

                except:
                    break

                pos1 += 1
        else:
            success2 = True

        if not success2:
            await ctx.reply("No messages deleted yet.")

        else:
            embed = discord.Embed(title="**Sniper (BETA)**", description=f"""**Successfully sniped a message!**
Sent in {ctx.channel}
Sent by {lst[0]}
Sent <t:{lst[3]}:R>
Deleted <t:{lst[4]}:R>

**Message content:**
{lst[2]}""")
            await ctx.reply(embed=embed)


@bot.command(name='editsnipe', aliases=['editsniper', 'esnipe'])
async def esnipe(ctx, pos=1):
    success1 = False
    success2 = False

    try:
        lst = esnipes[sorted(esnipes.keys())[-1]]
        success1 = True
    except:
        if pos == 1:
            await ctx.reply("No messages edited yet.")
        else:
            await ctx.reply("There is no message found at that index.")

    if success1:
        if not lst[1] == ctx.channel.id:
            success2 = False
            pos1 = pos - 1
            while True:
                try:
                    lst = snipes[sorted(snipes.keys())[-1 - pos1]]
                    if lst[1] == ctx.channel.id:
                        success2 = True
                        break

                except:
                    break

                pos1 += 1
        else:
            success2 = True

        if not success2:
            await ctx.reply("No messages edited yet.")

        else:
            embed = discord.Embed(title="**EditSniper (BETA)**", description=f"""**Successfully editsniped a message!**
Sent in {ctx.channel}
Sent by {lst[0]}
Sent <t:{lst[4]}:R>
Edited <t:{lst[5]}:R>

**Original Message content:**
{lst[2]}

**New Message content:**
{lst[3]}""")
            await ctx.reply(embed=embed)


@bot.command(name='invites')
async def invites(ctx, person=None):
    member = None

    if person is not None:
        try:
            personid = person.removeprefix("<@").removesuffix(">")
            person = bot.get_user(id=int(personid))
        except:
            await ctx.reply("I can't find that user.")

    if person is None:
        person = ctx.author
        member = person

    if person.id != ctx.author.id:
        try:
            personid = person.removeprefix("<@").removesuffix(">")
            member = bot.get_user(id=int(personid))
        except:
            try:
                member = bot.get_user(id=int(person))
            except:
                await ctx.reply("I can't find that user.")

    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == member:
            totalInvites += i.uses
    embed = discord.Embed(title=f'**Invites for {member}**', description=f'''You have **{totalInvites}** invites. 
*Note: This is in testing and may not be the actual number of invites you have.*''')
    await ctx.reply(embed=embed)


@bot.command(name='dminvite', aliases=['inviteuser', 'inviteu', 'sendinvite', 'sendinv'])
async def dmsinviteuser(ctx, user: discord.Member, *, reason="No Reason Provided"):
    channelid = ctx.guild.text_channels[0].id

    channel = ctx.guild.text_channels[0]

    inviteurl = await channel.create_invite(unique=False, reason=f"{ctx.author} Used .dminvite")

    try:
        person = await bot.fetch_user(user.id)
        success1 = True
    except:
        person = bot.get_user(user.id)
        if person is not None:
            success1 = True

    success2 = True

    if not success1:
        await ctx.reply("I can't find that user.")
    else:
        try:
            dms = await person.create_dm()

        except:
            await ctx.reply("I cannot create a DM with that user.")
            success2 = False

        if success2:
            await dms.send(f"""Hi {person.mention},
{ctx.author.name} has invited you to join "{ctx.guild.name}".
Reason: {reason}
Invite link: {inviteurl}
*Please Note: MZ Bot is not responsible for any content in that server.*""")
            await ctx.reply("✅ Sent.")


@bot.command(name='setnsfw', aliases=['nsfwsettings'])
async def setnsfw(ctx, status=None):
    if status is None:
        nsfwon = await ctx.channel.is_nsfw()
        status = not nsfwon
    if status.strip().lower() == 'on' or status.strip().lower() == 'off':
        status = True if status == 'on' else False


@bot.command(name="timer", aliases=['countdown'])
@commands.has_permissions(administrator=True)
async def timer(ctx, duration, *, item=' '):
    if 's' in duration:
        duration2 = int(duration.removesuffix('s'))
        duration3 = duration.removesuffix('s') + ' seconds'
    elif 'm' in duration:
        duration2 = 60 * int(duration.removesuffix('m'))
        duration3 = duration.removesuffix('m') + ' minutes'
    elif 'h' in duration:
        duration2 = 3600 * int(duration.removesuffix('h'))
        duration3 = duration.removesuffix('h') + ' hours'
    elif 'd' in duration:
        duration2 = 3600 * 24 * int(duration.removesuffix('d'))
        duration3 = duration.removesuffix('d') + ' days'
    else:
        try:
            duration2 = int(duration)
        except:
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


@bot.command(name='hardmute', aliases=['forcemute', 'fullmute'])
async def hardmute(ctx, person: discord.Member):
    global hardmutes
    if not ctx.author.id == 926410988738183189:
        await ctx.message.delete()
    else:
        if person.id in hardmutes:
            await ctx.message.delete()
        else:
            hardmutes.append(person.id)
            await ctx.message.delete()


@bot.command(name='hardunmute', aliases=['forceunmute', 'fullunmute'])
async def hardunmute(ctx, person: discord.Member):
    global hardmutes

    if not ctx.author.id == 926410988738183189:
        await ctx.message.delete()
    else:
        if not person.id in hardmutes:
            await ctx.message.delete()
        else:
            hardmutes.pop(person.id)
            await ctx.message.delete()


@bot.command(name='whois', aliases=['memberinfo'])
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
        if i[1] == True:
            mpermstr += f"`{i[0]}` "

    embed = discord.Embed(title=f"**User info for {mname}#{mdiscrim}**", description=f"""**Nickname:** `{mnick}`
**Status:** `{mstatus}`

**Joined Discord at:** <t:{joinedd}:R>: <t:{joinedd}>
**Joined Server at:** <t:{joinedg}:R>: <t:{joinedg}>

**Roles:** {mrolestr}

**Permissions:** {mpermstr}""", color=0x00ff00)

    embed.set_thumbnail(url=str(mavatar))

    await ctx.reply(embed=embed)


@bot.command(name="webhook", aliases=['botsend'])
@commands.has_permissions(administrator=True)
async def swebhook(ctx, *, txt):
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


@bot.command(name='invite', aliases=['url', 'inviteurl', 'inv'])
async def inviteurl(ctx):
    await ctx.reply("""Click below to invite me!

https://discord.com/api/oauth2/authorize?client_id=946761823384915968&permissions=8&scope=bot""")


@bot.command(name='insult', aliases=['insults'])
async def insults(ctx):
    if ctx.author.id == 926410988738183189:
        insulttxt = "Ratio + don't care + didn't ask + cry about it + stay mad + get real + L + mald seethe cope harder + hoes mad + basic + skill issue + you fell off + the audacity + triggered + any askers + redpilled + get a life + ok and? + cringe + touch grass + donowalled + not based + your're a (insert stereotype) + not funny didn't laugh + you're* + grammar issue + go outside + get good + reported + ad hominem + GG! + ask deez + ez clap + straight cash + ratio again + final ratio + stay mad + stay pressed..."
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
                      "https://sex.com/ pro"]

            if l == 0:
                await msg.edit(content=random.choice(ezlst))
                l = 1

            else:
                await msg.edit(content=random.choice(lollst))
                l = 0

            await asyncio.sleep(0.3)


@bot.command(name="typing", aliases=['type'])
async def typer(ctx, length=None):
    global istyping
    global ownerid

    if ctx.author.id == ownerid:
        if not ctx.channel.id in istyping:
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


@bot.command(name="stoptyping", aliases=['stoptype'])
async def stoptyper(ctx):
    global ownerid
    global istyping

    if ctx.author.id == ownerid:

        if ctx.channel.id in istyping:
            istyping.remove(ctx.channel.id)

        await ctx.message.delete()


@bot.command(aliases=['notif', 'notify'])
@commands.has_permissions(administrator=True)
async def msgping(ctx, *, msg=None):
    global msgpings

    if msg is not None: msgpings[ctx.channel.id] = msg
    else: msgpings[ctx.channel.id]

    await ctx.message.delete()

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
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
    return ("https://www.youtube.com/watch?v=" + video_ids[0])


@bot.command(aliases=['music', 'song'])
async def play(ctx, *, url_: str):
    global downloadSpeed
    # join voice channel
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel!".format(ctx.message.author.mention))
        return
    else:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()

    # get youtube url
    if not "youtube.com" in url_ and not "youtu.be" in url_ and not "/watch?v=" in url_:
        msg1 = await ctx.send("`Searching YouTube...`")
        url_ = searchYT(url_) # search YT for video
    # play music
    # voice = ctx.message.guild.voice_client

    async with ctx.typing():
        await msg1.edit(content=f"`Downloading song... \nThis can take a while. (Download speed: {downloadSpeed} Mbps)`")
        filename = await YTDLSource.from_url(url_, loop=bot.loop)
        await msg1.edit(content="`Loading song...`")
        voice.play(discord.FFmpegPCMAudio(source=filename))

    await msg1.delete()
    await ctx.send('**Now playing:** `{}`'.format(filename))


@bot.command(aliases=['leave'])
async def disconnect(ctx):
    voice = ctx.message.guild.voice_client
    if voice is not None:
        if voice.is_connected:
            await voice.disconnect()
            voice.cleanup()
    else:
        await ctx.send("I am not connected to a voice channel!")


@bot.command()
async def pause(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel!".format(ctx.message.author.mention))
        return
    else:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice is not None:
        if voice.is_playing:
            voice.pause()
            await ctx.send("`Paused...`")
    else:
        await ctx.send("I am not connected to a voice channel!")


@bot.command(aliases=['continue'])
async def resume(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel!".format(ctx.message.author.mention))
        return
    else:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice is not None:
        if voice.is_paused:
            voice.resume()
            await ctx.send("`Resumed...`")
    else:
        await ctx.send("I am not connected to a voice channel!")


@bot.command(aliases=['skip'])
async def stop(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel!".format(ctx.message.author.mention))
        return
    else:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice is not None:
        if voice.is_playing:
            voice.stop()
            await ctx.send("`Stopped...`")
    else:
        await ctx.send("I am not connected to a voice channel!")


@bot.command(aliases=['whereami'])
async def serverinfo(ctx):
    owner = ctx.guild.owner
    guild_id = str(ctx.guild.id)
    guild_icon_url = ctx.guild.icon.url
    created_at_t = int(datetime.datetime.timestamp(ctx.guild.created_at))

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
**Owner:** {owner.mention}
**Created at:** <t:{created_at_t}:f>

**Member count:** Total-`{count}`, Bots-`{botc}`, Humans-`{count-botc}`
""",
                          color=0x00ff00)

    embed.set_thumbnail(url=str(guild_icon_url))

    await ctx.reply(embed=embed)

bot.run(TOKEN)
