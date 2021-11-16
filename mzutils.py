import discord
import datetime
import random
import asyncio
from discord.ext import commands
import os

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
    
      if secs >= 60:
          answer='{} mins and {} secs'.format(int(mins),secs)
          if mins >= 60:
              answer='{} hrs, {} mins and {} secs'.format(int(hrs),int(mins),secs)
              if hrs >= 24:
                  answer='{} days, {} hrs, {} mins and {} secs'.format(int(days),int(hrs),int(mins),secs)
      return answer
  
def timestr(secs, mins=0, hrs=0, days=0):
    if secs >= 60:
        answer='{} mins and {} secs'.format(int(mins),secs)
        if mins >= 60:
            answer='{} hrs, {} mins and {} secs'.format(int(hrs),int(mins),secs)
            if hrs >= 24:
                answer='{} days, {} hrs, {} mins and {} secs'.format(int(days),int(hrs),int(mins),secs)
    
    return answer
  
def filewrite(filename, msg):
  workinprogress=True
