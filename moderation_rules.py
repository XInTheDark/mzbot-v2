"""Special moderation rules"""
import discord  # discord.py
import asyncio
import openai, os  # OpenAI API for moderation

def openAIinit(envName="OPENAI_API_KEY"):
    openai.api_key = os.getenv(envName)
    return openai.api_key  # returns None if key not found.

openAIinit()

"""Constants"""
whitelist_servers = [996407200161472542, 1076679987773591643]
openai_moderate_servers = [996407200161472542, 1083361948181213294] # servers to run openAI's moderation endpoint on

# Spam command related
spam_ban = [726356086176874537]  # banned from using spam commands
spam_whitelist = [926410988738183189]  # cannot be DMSpammed

async def moderate(message: discord.Message):
    """Moderate a message."""
    
    # This is where you can add your moderation rules.

    msg = message.content
    
    # OpenAI moderation
    if message.guild.id in openai_moderate_servers\
            and not message.author.guild_permissions.administrator:
        response: bool = openai.Moderation.create(
            input=msg
        )["results"][0]["flagged"]
        
        if response:
            await message.delete()
            return True
        
    
