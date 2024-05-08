# imports
from datetime import *
from configs import *

# variables
uptime = 0
checkInterval = 300
#os.system('export $MCRCON_PASS=passcode')

# functions
def getHour():
    x = datetime.strptime("11/03/22 14:23", "%d/%m/%y %H:%M")
    return eval(str(x.time())[0:2])

def getSeed():
    try:
        seedline = f'SEED = {rcon("seed")[9:-6]}\n'
        configs = open('configs.py','r')
        lines = configs.readlines()
        for line in range(len(lines)):
            if lines[line][0:4]=='SEED':
                lines[line] = seedline
                break
        configs = open('configs.py','w')
        configs.writelines(lines)
        configs.close()
    except:
        print('Error fetching seed.')
    
def formatUptime(uptime):
    utH = int((uptime-(uptime%3600))/3600)
    utM = int((uptime-(uptime%60))/60)%60
    utS = int(uptime%60)
    if utH<10:
        utH = "0"+f"{utH}"
    if utM<10:
        utM = "0"+f"{utM}"
    if utS<10:
        utS = "0"+f"{utS}"
    return f'{utH}:{utM}:{utS}'

async def waitInterval(checkInterval):
    global uptime
    for seconds in range(checkInterval):
        await asyncio.sleep(1)
        uptime += 1

        if uptime%30==0 and not online():
            return

        os.system(cls())
        print(f'Server RCON Status: Up\nServer uptime: {formatUptime(uptime)}')

async def checkall():
    if os.path.exists('stopping.txt'):
        os.remove('stopping.txt')
        return
    if not online():
        log(f'Server crashed on {getdt()}.\n')
        await mcinit('AUTO-OTTO')
        exit()
    else:
        playercount = eval(stats()['numplayers'])
        #hour = getHour()
        if playercount==0:
            savestop()
    
# code
async def main():
    global uptime
    os.system(f'{title("MCRCON")}')
    os.chdir(f'{PATH}{slash()}Tiko-bot')
    print('Waiting for server to start...')
    await asyncio.sleep(15)
    if OS=="Linux":
        while not online():
            os.system(cls())
            print('Waiting for server to start...')
            await asyncio.sleep(2)
    print('Remotely connecting...')
    #check seed
    getSeed()
    #initiate scoreboard object
    #rcon("scoreboard objectives add players dummy")
    os.remove('starting.txt')
    # set difficulty
    rcon(f"difficulty {DIFF}")

    while online():
        await waitInterval(checkInterval)
        await checkall()
        if not online():
            break #redundant but seems to save 5 mins of rcon runtime for some reason

    log(f'Server stopped automatically on {getdt()}. (Uptime: {formatUptime(uptime)})\n')
    exit()

# run
asyncio.run(main())