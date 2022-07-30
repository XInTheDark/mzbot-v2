import discord
import datetime
import random
import asyncio
from discord.ext import commands
import os
import psutil

bannedWords = [
    'jiang muzhen',
    'crush',
    'muzhen irl'
]

def snowflake(id: int):
    snowflake_time = discord.utils.snowflake_time(int(id1))
    return snowflake_time

def timedif(id1: int, id2: int, secs=True):
    time1 = discord.utils.snowflake_time(int(id1))
    time2 = discord.utils.snowflake_time(int(id2))
    ts_diff = time2 - time1
    secs = abs(ts_diff.total_seconds())
    
    if secs:
        return secs
    else:
        days,secs=divmod(secs,secs_per_day:=60*60*24)
        hrs,secs=divmod(secs,secs_per_hr:=60*60)
        mins,secs=divmod(secs,secs_per_min:=60)
        secs=round(secs, 2)
        answer='{} secs'.format(secs)
        
        return answer
        
def timestr(secs, mins=0, hrs=0, days=0):
    secs = int(secs)
    days,secs=divmod(secs,secs_per_day:=60*60*24)
    hrs,secs=divmod(secs,secs_per_hr:=60*60)
    mins,secs=divmod(secs,secs_per_min:=60)
    
    secs = round(secs, 2)
    
    answer = f"{secs} secs"
    if mins > 0:
        answer='{} mins and {} secs'.format(int(mins),secs)
    if hrs > 0:
        answer='{} hrs, {} mins and {} secs'.format(int(hrs),int(mins),secs)
    if days > 0:
        answer='{} days, {} hrs, {} mins and {} secs'.format(int(days),int(hrs),int(mins),secs)
    
    return answer

def filewrite(filename, msg):
  workinprogress=True


def sysinf():
    
    vcpu="Used CPU: " + str(psutil.cpu_percent()) + "%"
    
    y = round(100 - (psutil.virtual_memory().available * 100 / psutil.virtual_memory().total), 5)
    z = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 5)
    
    usedram = 'Used RAM: '+ str(y) + '%'
    availram = 'Available RAM: ' + str(z) + '%'
    
    return [vcpu, usedram, availram]
