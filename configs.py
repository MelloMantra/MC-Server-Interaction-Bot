# Configuratons

# imports
import random
from time import time
from time import sleep
import discord
import discord.utils
from discord.utils import get
from discord.ext import commands, bridge
from discord.commands import Option
from discord.ext import tasks
import datetime as dt
import os.path
import os
import re
import public_ip as ip
import platform
from mctools import *
import asyncio
import subprocess

# linux accomodations and other functions

def getdt():
    currTime = dt.datetime.now()
    strDate = currTime.strftime('%A, %B %d, %Y')
    strTime = currTime.strftime('%I:%M:%S %p')
    return f'{strDate} at {strTime}'

def start(file):
    if not OS=='Linux':
        os.startfile(file)
    else:
        #subprocess.call(['gnome-terminal','--','python3',file,'&'])
        os.system(f'xdg-open {file}')

def log(msg):
    log = open('log.txt','a')
    log.write(msg)
    log.flush()
    os.fsync(log.fileno())
    log.close()

async def mcinit(author):
    log(f'Server started by {author} on {getdt()}.\n')
    starting = open('starting.txt','x')
    starting.close()
    start('mcstart.py')
    start('rcon.py')

def slash():
    return "\\" if not OS=='Linux' else "/"

def delete():
    return "del" if not OS=='Linux' else "rm"

def cls():
    return "cls" if not OS=='Linux' else "clear"

def title(title):
    return f"@echo off && title {title}" if not OS=='Linux' else rf"""PROMPT_COMMAND='echo -ne "\033]0;{title}\007"'"""

def ipget():
    temp = ""
    while re.search("\.",temp)==None:
        temp = ip.get(1)
    return temp

def rcon(cmds):
    rcon = RCONClient('localhost')
    rcon.login(RPWD)
    if type(cmds) is list:
        response = []
        for cmd in cmds:
            response.append(rcon.command(cmd))
            sleep(1)
    else:
        response = rcon.command(cmds)
    rcon.stop()
    return response

def stats():
    query = QUERYClient('localhost')
    stats = query.get_full_stats()
    query.stop()
    return stats

def savestop():
    stopping = open('stopping.txt','x')
    stopping.close()
    rcon(['save-all','stop'])

def mcping():
    ping = PINGClient('localhost',PORT)
    lat = round(ping.ping(),3)
    ping.stop()
    return lat

def online():
    rcon = RCONClient('localhost')
    try:
        rcon.login(RPWD)
        res = rcon.is_authenticated()
        rcon.stop()
        return res
    except:
        rcon.stop()
        return False

# global vars
OS = platform.system()
PATH = "C:\\Users\\user\\Desktop\\Tiko" if not OS=='Linux' else '/home/raspi/Desktop/Tiko' # example paths
ISREPO = True # boolean for if Tiko is operating in a cloned git repo

# mc server vars
MCSERVERIP = ipget()
PORT = 25565 # port mc server runs on
MCVERSION = "1.20.4"
MCWORLD = "Survival World"
RAM = 4000
BTYPE = "M" # M for megabytes (mc server ram)
SEED = 1111111111111111111
RPWD = 'password' # rcon password
DIFF = "hard"

# bot vars
TOKEN = "token" # bot token
OWNER = 111111111111111111 # owner's user ID
LOG = 111111111111111111 # log channel ID
