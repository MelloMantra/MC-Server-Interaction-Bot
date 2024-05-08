# import configs
from configs import *

os.chdir(f'{PATH}{slash()}Tiko-bot')
PID = str(os.getpid())

# functions
async def mcstop(msg):
    try:
        playercount = eval(stats()['numplayers'])
    except Exception as error:
        print(error)
        playercount = 0
        pass
    if playercount>0:
        rcon(f"say {msg}")
        await asyncio.sleep(19)

    savestop()
    os.chdir(f'{PATH}{slash()}Tiko-bot')
    if os.path.exists('starting.txt'): os.remove('starting.txt')
    log(f'Server stopped manually on {getdt()}.\n')

def fkill():
    savestop()
    if os.path.exists('starting.txt'): os.remove('starting.txt')
    log(f'Server stopped (forcefully) on {getdt()}.\n')

def pull():
    os.chdir(f'{PATH}{slash()}Tiko-bot')
    mcon = os.path.exists('starting.txt')
    os.system('git reset --hard')
    os.system('git clean -fd')
    os.system('git pull --no-rebase')
    if mcon:
        starting = open('starting.txt','x')
        starting.close
    temp = open('temp.txt','x')
    temp.write(str(PID))
    temp.close

def push(desc:str='.',file:str=''):
    os.chdir(f'{PATH}{slash()}Tiko-bot')
    if os.path.exists('temp.txt'): os.remove('temp.txt')
    if os.path.exists('starting.txt'): os.remove('starting.txt')
    if file=='':
        os.system(f'git add .')
    os.system(f'git commit -m {desc} {file}')
    os.system('git push origin main')

async def restartBot(mode='/s'):
    mcon = False
    if os.path.exists("starting.txt"):
        while os.path.exists("starting.txt"):
            await asyncio.sleep(1)
    if online():
        mcon = True
        await mcstop("Tiko and server performing routine restart in 20 seconds...")
    temp = open("temp.txt","w") if os.path.exists('temp.txt') else open('temp.txt','x')
    temp.write(str(mcon))
    temp.close()
    log(f'Bot restarted on {getdt()}.\n')
    if mode=='/h' and OS=="Linux":
        os.system("sudo reboot")
    else:
        start('bot.py')
    exit()
    
isFirst = True

class Tiko(bridge.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.messages = True
        intents.message_content = True
        intents.bans = True

        description = '''A bot that (among other things) allows Discord users to activate a Minecraft Server, written in Python by Mello Mantra. Currently not publicly available.\nMore info: https://bit.ly/3ByWea7\nDefinitely not addicted to crystal meth and high as hell all the time'''
        status = discord.Status.online
        activity = discord.Activity(type=discord.ActivityType.listening, name='beats to photosynthesize to // .help')

        super().__init__(command_prefix='.', intents=intents, description=description, status=status, activity=activity)

    async def on_ready(self):
        os.system(f'{title("Tiko")}')
        print('PID: '+PID)
        os.chdir(f'{PATH}{slash()}Tiko-bot')
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        if not os.path.exists('log.txt'):
            log = open('log.txt','x')
            log.write('==============\nTIKO AUDIT LOG\n==============\n')
            log.close()
        if os.path.exists('temp.txt'):
            temp = open("temp.txt","r")
            mcon = temp.read()
            temp.close()
            if mcon=="True":
                await mcinit('AUTO-OTTO')
        if ISREPO:
            restart.start()
        print('------')

        #bot.add_view(verifybutton())

# variables & stuff

bot = Tiko()
owner = bot.get_user(OWNER)
mcsleep = False

@tasks.loop(hours=24.0)
async def restart():
    global isFirst
    if isFirst:
        isFirst = False
        if OS!="Linux":
            push()
        pull()
        return
    else:
        await restartBot('/h')

# global commands & stuff
@bot.bridge_command(description="Knock on Tiko's hollow noggin")
async def ping(ctx):
    '''Knock on Tiko's hollow noggin'''

    print('Bot pinged.')
    await ctx.respond(f'pongers `{round(bot.latency,3)}s`')

# MINECRAFT SERVER COG
class mcserver(commands.Cog, name='Minecraft-Server'):
    '''Commands relating to the Minecraft server.'''
    def __init__(self,bot):
        self.bot = bot

    #mc
    @commands.command(description="Returns info about the Minecraft server")
    async def mc(self, ctx, arg:str=None):
        '''Returns info about the Minecraft server.
        Use /a argument for advanced info.'''
        global mcsleep

        print('Server status requested.')
        message = await ctx.reply('Fetching stats...')
        if os.path.exists('starting.txt'):
            status = 'starting'
        elif online():
            status = 'online'
        elif mcsleep:
            status = 'asleep'
        else:
            status = 'offline'
        version = MCVERSION
        appendage = ''

        try:
            if status=='online' and online():
                stat = stats()
                version = stat['version']
                playercount = eval(stat['numplayers'])
                maxplayers = stat['maxplayers']
                playerlist = '\n'.join(stat['players']) if playercount>0 else 'None'
                for player in playerlist:
                    player = player[:-4]
                difficulty = re.split('The difficulty is ',rcon("difficulty"),1)[1][:-4]
                latency = mcping()
                seed = rcon("seed")[7:-5]
            else:
                playercount = 0
                maxplayers = 20
                playerlist = 'None'
                difficulty = 'Unknown'
                latency = 0
                seed = SEED


            #brief
            if arg=='/b':
                if status=='online':
                    statemo = '🟢'
                elif status=='offline':
                    statemo = '🔴'
                elif mcsleep:
                    statemo = '🌙'
                else:
                    statemo = '🔃'
                await message.edit(f'**{statemo} | {playercount}/{maxplayers} players**')
                return

            #advanced info
            if arg=='/a':
                appendage = f'\n**Seed:** {seed}\n**Current world style:** {MCWORLD}\n**Difficulty:** {difficulty}\n**RAM Allocated:** {RAM}{BTYPE}B\n**Latency:** `{latency}s`\n**Players:** ```\n({playercount}/{maxplayers})\n{playerlist}```'
        except IndexError:
            pass
        except Exception as error:
            print(error)
            await message.edit(f'Error: {error}')

        await message.edit(f'''The Minecraft server is currently **{status}**.\n**IP:** {MCSERVERIP}:{PORT}\n**Version:** {version}{appendage}''')

    #start
    @bridge.bridge_command(description="Starts the Minecraft server")
    async def start(self, ctx):
        '''Starts the Minecraft server.'''
        global mcsleep
        if mcsleep:
            await ctx.respond("Server currently asleep.")
            return

        if os.path.exists('starting.txt') or online():
            print('Server start request recieved...\nError: Server already running!')
            await ctx.respond('Server start request recieved...\nError: Server already running!')
        else:
            wait = 60 if OS=="Linux" else 15
            print(f'Server start request recieved...\nServer starting in {wait} seconds!')
            await ctx.respond(f'Server start request recieved...\nServer starting in {wait} seconds!')
            await mcinit(ctx.author.name)

    #kill
    @bridge.bridge_command()
    #@bridge.has_permissions(administrator=True)
    async def kill(self, ctx, option:str=None):
        '''Stops the server differently (Admin only, see help menu for usage)
    
    Options:
    
    /f -- Forces the Minecraft server to save & quit instantly.
    /s -- Forces the Minecraft server to save & quit instantly and enters sleep mode. While sleep mode is active, all commands in the Minecraft Server cog will be disabled (besides mc and kill).
    /w -- Wakes the Minecraft server from sleep mode.'''
        if ctx.author.id!=OWNER:
            await ctx.reply("You don't have permission to do that.")
            return
        global mcsleep

        try:
            if os.path.exists('starting.txt'):
                await ctx.reply('Error: Unable to connect to server.')
                return
            
            if option=='/f':
                if online():
                    print('Server stopping...')
                    await ctx.reply('Server stopping...')
                    fkill()

                else:
                    print('Server stop request recieved...\nError: Server is already off!')
                    await ctx.reply('Server stop request recieved...\nError: Server is already off!')
                    return
            elif option == '/s':
                if mcsleep:
                    await ctx.reply('Server already asleep!')
                    return
                if online():
                    print('Server stopping...')
                    await ctx.reply('Server sleep request recieved. Stopping server...')
                    fkill()
                
                mcsleep = True
                print('mcsleep enabled')
                log(f'Server entered sleep mode on {getdt()}.')
                await ctx.reply('The server has entered sleep mode. All corresponding commands will be ignored until further notice.')
            elif option == '/w':
                if mcsleep:
                    mcsleep = False
                    print('mcsleep disabled')
                    log(f'Server awoken on {getdt()}.')
                    await ctx.reply('Minecraft server has been awoken.')
                else:
                    await ctx.reply("The server isn't asleep!")
        except IndexError:
            await ctx.reply("It appears as if you didn't include any arguments, dude. Use `.help kill` for command help.")
        except Exception as error:
            print(error)
            await ctx.reply(f'Error: {error}')

    #stop
    @bridge.bridge_command()
    #@bridge.has_permissions(administrator=True)
    async def stop(self, ctx):
        '''Stops the Minecraft server. (Admin only)'''
        global mcsleep
        if mcsleep:
            await ctx.reply("Server currently asleep.")
            return
        if ctx.author.id!=OWNER:
            await ctx.reply("You don't have permission to do that.")
            return
        if os.path.exists('starting.txt'):
            await ctx.reply('Error: Unable to connect to server.')
            return

        if online():
            print('Server stopping...')
            await ctx.reply('Server stopping...')
            await mcstop("Manual shutdown initiated; server stopping in 20 seconds.")
        else:
            print('Server stop request recieved... Error: Server is already off!')
            await ctx.reply('Server stop request recieved... Error: Server is already off!')

    #cli
    @bridge.bridge_command()
    #@bridge.has_permissions(administrator=True)
    async def cli(self, ctx, arg:str=None):
        '''Interacts with the Minecraft server CLI. (Admin only)
           If arg includes a space then it must be enclosed in quotation marks.'''

        if arg==None:
            await ctx.respond('You forgot your argument, bud. Use `.help cli` for more info.')
            return
        if ctx.author.id!=OWNER:
            await ctx.respond("You don't have permission to do that.")
            return
        if os.path.exists('starting.txt'):
            await ctx.reply('Error: Unable to connect to server.')
            return
        
        if online():
            output = rcon(arg)[:-4]
            if output!='':
                await ctx.respond(f"Output: `{output}`")
            await ctx.send(f"Successfully executed `{arg}`!")
        else:
            await ctx.respond('Error: Minecraft server offline.')

    #world
    @bridge.bridge_command()
    #@bridge.has_permissions(administrator=True)
    async def world(self, ctx, option):
        '''Manipulates the Minecraft world. (Admin only)'''

        if not option:
            await ctx.respond('You forgot your argument, bud. Use `.help world` for more info.')
            return
        if ctx.author.id!=OWNER:
            await ctx.respond("You don't have permission to do that.")
            return

        #new world option
        if option=='/n':
            size = 0
            for path, dirs, files in os.walk(f'{PATH}{slash()}MC-Server{slash()}world'):
                for f in files:
                    fp = os.path.join(path, f)
                    size += os.path.getsize(fp)
            size = size/(1024*1024)
            message = await ctx.respond(f'''You're about to delete the current Minecraft world ({size}). Are you sure you want to continue? (y/n)''')
            await asyncio.sleep(10)


        #switch world option
        #print('World swapped')
        #ctx.respond('World swapped.')
        pass
    
    #log
    @bridge.bridge_command(description='Displays the last x lines of the log file.')
    @bridge.has_permissions(administrator=True)
    async def log(self, ctx, lines:int=1):
        '''Displays the last x lines (default 1) of the log file. (Admin only)'''
        log = open(f'{PATH}{slash()}Tiko-bot{slash()}log.txt')
        content = log.readlines()
        result = ''
        for line in range(lines):
            result = f'{content[len(content)-(line+1)]}\n{result}'
        await ctx.respond(f'Last **{lines}** line(s) of log file:\n```\n{result}```')

    #motd
    @bridge.bridge_command()
    #@bridge.has_permissions(administrator=True)
    async def motd(self, ctx, *motd):
        '''Edits the Minecraft server's MOTD. (Admin only)'''

        if ctx.author.id!=OWNER:
            await ctx.respond("You don't have permission to do that.")
            return
        
        try:
            if motd[0]: motd = ' '.join(motd)
        except:
            motd = '\n'

        sp = open(f'{PATH}{slash()}MC-Server{slash()}server.properties','r+')
        lines = sp.readlines()
        sp.close()
        for i in range(len(lines)):
            if lines[i][0:5]=='motd=':
                currmotd = lines[i][5:]
                motdline = i
                break
        if motd!='':
            lines[motdline] = f'motd={motd}\n'
            sp = open(f'{PATH}{slash()}MC-Server{slash()}server.properties','w')
            sp.writelines(lines)
            sp.close()
            await ctx.reply(f'Successfully changed previous motd `{currmotd}` to `{motd}`.')
        else:
            await ctx.reply(f'Current motd: `{currmotd}`')            

# ADMIN COMMANDS
class admin(commands.Cog, name='Administrator'):
    '''Commands that only admins can execute. Slash commands are not supported for this cog.'''
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def push(self, ctx, desc:str='.', file:str='.'):
        '''Push all current files to the GitHub repository.
        
Arguments:

push <custom description> - Set a custom description for the commit (double quotes optional)(optional parameter)'''
        if not ctx.author.id==OWNER and not ctx.guild: return
        #await ctx.message.delete()

        try:
            message = await ctx.respond('Updating files...')
            push(desc,file)
            await message.edit('Committed all current files to the GitHub repository.')

            channel = bot.get_channel(LOG)
            await channel.send(f'All files committed to GitHub repo on {getdt()}.')

            print('Committed files to GitHub repository.')
        except Exception as error:
            print(error)
            await ctx.send(f'Error: {error}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def pull(self, ctx):
        '''Update files from the GitHub repository.'''

        message = await ctx.respond('Fetching latest files...')
        pull()
        push('Merge')
        HEAD = subprocess.run(['git','reset','--hard'],stdout=subprocess.PIPE).stdout.decode()
        await message.edit(f'Synchronous with the GitHub repository as of {getdt()}.\n```{HEAD}```\nIssue `.restart` to enact changes.')

        channel = bot.get_channel(LOG)
        await channel.send(f'Synchronous with the GitHub repository as of {getdt()}.\n```{HEAD}```')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx, mode=''):
        '''Restarts Tiko.
        If used with /h option (hard reset), reboots Raspberry Pi.'''
        if ctx.author.id!=OWNER:
            await ctx.reply("You don't have permission to do that.")
            return
        await ctx.reply("Restarting bot...")
        if OS=='Linux':
            pull()
        await restartBot(mode)

    @commands.command()
    #@commands.has_permissions(administrator=True)
    async def sh(self,ctx,cmd='',*args):
        '''Executes cmd in the system CLI.'''
        if ctx.author.id!=OWNER:
            await ctx.reply('Nice try.')
            return
        if cmd=='':
            await ctx.reply('Maybe try actually using a command next time, homie.')
            return
        force = False
        bypass = False
        if cmd=='/f':
            force = True
            cmd = args[0]
        elif cmd=='/b':
            bypass = True
            cmd = args[0]

        line = [cmd]
        for arg in args:
            if (not force and not bypass) or arg!=args[0]:
                line.append(arg)
        message = await ctx.reply(f'Executing `{" ".join(line)}`...')

        if not bypass:
            try:
                result = subprocess.run(line,stdout=subprocess.PIPE).stdout.decode()
            except Exception as error:
                await message.edit(f'Error occurred while executing `{" ".join(line)}`:\n```{error}```')
                if force:
                    try:
                        os.system(' '.join(line))
                        await message.edit(f'Error occurred while executing `{" ".join(line)}`, but forced execution was successful.')
                    except:
                        pass
                return
        else:
            try:
                os.system(' '.join(line))
                result = 'Unable to retrieve output.'
            except Exception as berror:
                await message.edit(f'Error occurred while executing `{" ".join(line)}`:\n```{berror}```')
                return
        if result=='':
            result = 'None'
        await message.edit(f'Successfully executed `{" ".join(line)}` in {OS} terminal.\nOutput:\n```{result}```')

# Cogs
bot.add_cog(mcserver(bot))
bot.add_cog(admin(bot))

# Run    :D
bot.run(TOKEN)
