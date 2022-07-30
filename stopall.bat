@echo off

mcrcon -p passcode -w 20 "say Manual shutdown initiated; server stopping in 20 seconds." save-all
mcrcon -p passcode stop
timeout /t 3 /nobreak
del on.txt
echo Server stopped (manually) on %date% at %time%. >>log.txt
taskkill /f /im cmd.exe
taskkill /f /im cmd.exe
exit
