from configs import *
os.system(f'{title("Server-CLI")}')
os.chdir(f'{PATH}{slash()}MC-Server')
os.system(f"java -Xmx{RAM}{BTYPE} -Xms{RAM}{BTYPE} -jar server.jar nogui")