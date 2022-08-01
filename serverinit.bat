@echo off
cd "C:\Users\mgdr0\Desktop\Code\MC Server starter"
echo Server started on %date% at %time%. >>log.txt
echo. >>on.txt
start /min rcon.bat
start /min /wait startmcserver.bat
exit