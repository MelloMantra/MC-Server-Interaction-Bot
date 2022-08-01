#start maintain script first and foremost
import os
import tracemalloc
os.startfile("maintainStart.lnk")

#async definitions as well idrk
from discord import Webhook
import aiohttp
import asyncio

async def runningResponse():
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url='https://discord.com/api/webhooks/1003143955375992982/kvR632d4DmeZncskRgH6IHvOCHxhjD6JPji7i6enJEM8u_CJs8OaiNucsYDZeSGLlcBi', session=session)
    await webhook.send(content='Start request recieved... Error: Server already running!', username='Big SMP')

async def startingResponse():
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url='https://discord.com/api/webhooks/1003143955375992982/kvR632d4DmeZncskRgH6IHvOCHxhjD6JPji7i6enJEM8u_CJs8OaiNucsYDZeSGLlcBi', session=session)
    await webhook.send(content='Start request recieved... Server starting in 10 seconds!', username='Big SMP')

#imports
import cmd
from re import sub
import os.path
import websocket 
import json
import threading
import time
import subprocess

#function definitions
def sendJsonRequest(ws, request):
    ws.send(json.dumps(request))

def recieveJsonResponse(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print('Heartbeat initiated')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            'op': 1,
            'd': 'null'
        }
        sendJsonRequest(ws, heartbeatJSON)
        print('Heartbeat sent')
        
        #deprecated auto-shutdown scripting

        #print(time.localtime())
        #subprocess.run(r"C:\Users\mgdr0\Desktop\Code\Discord macros\MC Server starter\inactivitylogger.bat", shell=True)

#connect websocket, heartbeat timing, payload, token
ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieveJsonResponse(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = 'NDQyNDIxNjE2ODk5NjUzNjg0.GDwRv4._KyL8PPwu8KBM9JvsjxvMa7If5jjMgfPkeC518'
payload = {
    'op': 2,
    'd': {
        'token': token,
        'properties': {
            '$os': 'windows',
            '$browser': 'opera gx lmao',
            '$device': 'pc'
        }
    }
}

#request all message payloads
sendJsonRequest(ws, payload)

while True:
    event = recieveJsonResponse(ws)

    try:
        if f"{event['d']['content']}"=='.start bigsmp':
            print('Server start request recieved')
            if os.path.exists('on.txt'):
                print('Server already running!')

                runningResponse()

            else:
                print('Starting server...')

                startingResponse()

                subprocess.run("serverinit.bat", shell=True)
        opCode = event('op')
        if opCode==11:
            print('Heartbeat recieved')
    except:
        pass

#agacsvndfjhsagnedvfhjsdfr

