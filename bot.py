#imports
import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands
import aiohttp
import asyncio
import os.path
import os

#preliminary variables

description = '''**A bot that allows Discord users to activate a Minecraft Server.**
Currently not publicly available.
Prefix:  .
Definitely not addicted to crystal meth and high as hell all the time'''

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='.', intents=intents, description=description)

#definitions

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def ping(ctx):
    await ctx.send('pongers')

@bot.command()
async def mcstart(ctx):
    if os.path.exists(f'C:\\Users\\mgdr0\\Desktop\\Code\\MC Server starter\\on.txt'):
        print('Server start request recieved... Error: Server already running!')
        await ctx.send('Server start request recieved... Error: Server already running!')
    else:
        print('Server start request recieved... Server starting in 10 seconds!')
        await ctx.send('Server start request recieved... Server starting in 10 seconds!')
        os.startfile(f'C:\\Users\\mgdr0\\Desktop\\Code\\MC Server starter\\serverinit.bat')

@bot.command()
async def mckill(ctx):
    if os.path.exists(f'C:\\Users\\mgdr0\\Desktop\\Code\\MC Server starter\\on.txt'):
        print('Server stopping...')
        await ctx.send('Server stopping...')
        os.startfile(f'C:\\Users\\mgdr0\\Desktop\\Code\\MC Server starter\\stopall.bat')
    else:
        print('Server stop request recieved... Error: Server is already off!')
        await ctx.send('Server stop request recieved... Error: Server is already off!')

# run
bot.run('token')
