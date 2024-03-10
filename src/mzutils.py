import discord
import psutil

bannedWords = []


def removeprefix(s, prefix):
    """
    Useful for python < 3.9
    """
    if s.startswith(prefix):
        return s[len(prefix):]
    return s


def removesuffix(s, suffix):
    if s.endswith(suffix):
        return s[:-len(suffix)]
    return s


def snowflake(id1: int):
    """
    Returns snowflake time.
    """
    snowflake_time = discord.utils.snowflake_time(id1)
    return snowflake_time


def timedif(id1: int, id2: int, secs=True):
    time1 = discord.utils.snowflake_time(int(id1))
    time2 = discord.utils.snowflake_time(int(id2))
    ts_diff = time2 - time1
    secs = abs(ts_diff.total_seconds())
    
    if secs:
        return secs
    else:
        days, secs = divmod(secs, secs_per_day := 60 * 60 * 24)
        hrs, secs = divmod(secs, secs_per_hr := 60 * 60)
        mins, secs = divmod(secs, secs_per_min := 60)
        secs = round(secs, 2)
        answer = '{} secs'.format(secs)
        
        return answer


def timestr(secs, mins=0, hrs=0, days=0):
    secs = int(secs)
    days, secs = divmod(secs, secs_per_day := 60 * 60 * 24)
    hrs, secs = divmod(secs, secs_per_hr := 60 * 60)
    mins, secs = divmod(secs, secs_per_min := 60)
    
    secs = round(secs, 2)
    
    answer = f"{secs} secs"
    if mins > 0:
        answer = '{} mins and {} secs'.format(int(mins), secs)
    if hrs > 0:
        answer = '{} hrs, {} mins and {} secs'.format(int(hrs), int(mins), secs)
    if days > 0:
        answer = '{} days, {} hrs, {} mins and {} secs'.format(int(days), int(hrs), int(mins), secs)
    
    return answer


def filewrite(filename, msg):
    workinprogress = True


def sysinf():
    vcpu = "Used CPU: " + str(psutil.cpu_percent()) + "%"
    
    y = round(100 - (psutil.virtual_memory().available * 100 / psutil.virtual_memory().total), 5)
    z = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 5)
    
    usedram = 'Used RAM: ' + str(y) + '%'
    availram = 'Available RAM: ' + str(z) + '%'
    
    return [vcpu, usedram, availram]


def parseTime(duration: str):
    """
    Parse a time string.
    Returns an integer value in seconds. Returns None if parsing failed.
    Limited support as of now.
    """
    if not duration:
        return None
    
    duration2 = None
    
    if 's' in duration:
        duration2 = int(removesuffix(duration, 's'))
    elif 'm' in duration:
        duration2 = 60 * int(removesuffix(duration, 'm'))
    elif 'h' in duration:
        duration2 = 3600 * int(removesuffix(duration, 'h'))
    elif 'd' in duration:
        duration2 = 3600 * 24 * int(removesuffix(duration, 'd'))
    
    return duration2
