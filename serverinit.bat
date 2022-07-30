@echo off
echo Server started on %date% at %time%. >>log.txt
echo. >>on.txt
start /min rcon.bat
start /min /wait startmcserver.bat
exit