"""Special moderation rules"""
import discord  # discord.py
import asyncio

"""Constants"""
whitelist_servers = [996407200161472542, 1076679987773591643]

# Spam command related
spam_ban = [726356086176874537]  # banned from using spam commands
spam_whitelist = [926410988738183189]  # cannot be DMSpammed

async def moderate(message: discord.Message):
    """Moderate a message."""
    
    # This is where you can add your moderation rules.

    msg = message.content
    if "owo" in msg and "<@926410988738183189>" in msg:  # owner ID
        await message.delete()  # first delete this message,
        await asyncio.sleep(1)  # OwO bot is laggy, perhaps need a long(er) delay
        # If OwO follows up with a message, we delete that message as well.
        new_msg = [m async for m in message.channel.history(limit=1)][0]
        if new_msg.author.id == 408785106942164992:  # OwO bot ID
            await new_msg.delete()
