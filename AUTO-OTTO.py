# runs on RasPi boot
import os
import os.path
from configs import PATH
os.chdir(f'{PATH}/Tiko-bot')
if os.path.exists('temp.txt'):
    temp = open('temp.txt','r')
    pid = temp.read().strip('\n')
    temp.close()
    try:
        pid = eval(pid)
    except SyntaxError:
        pass
    if type(pid)!=int:
        os.system('sudo reboot')
    try:
        os.kill(pid,0)
    except:
        os.system('sudo reboot')
else:
    os.system('sudo reboot')