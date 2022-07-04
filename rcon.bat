@echo off

:: wait for server to start
timeout /t 6 /nobreak

::mcrcon -p passcode "scoreboard objectives add players dummy"

:stopcheck

:: wait 10 minutes
cls
timeout /t 600 /nobreak

:: check for players
for /f "delims=" %%g in ('mcrcon -p passcode "execute store result score objective players if entity @e[type=minecraft:player]"') do (
    set output=%%g
    set playercount=%output:~-1%
)

:: get current hour
for /f %%a in ('Powershell -Nop -c "Get-Date -Format 'HH'"') do set getcurrHour=%%a
set /a "hour=(1%getcurrhour%-100)"

:: playercount-based shutdown
if %playercount%==d (
    mcrcon -p passcode -w 3 save-all stop
    taskkill /f /im py.exe
    taskkill /f /im python.exe
    if %hour% lss 23 and %hour% gtr 8 (
        timeout /t 1 /nobreak
        start /min main.py
    )
    del on.txt
    taskkill /f /im cmd.exe
)

:: time-based shutdown
if %hour% gtr 22 (
    if not %playercount%==d (
        mcrcon -p passcode "say The server is shutting down for the day in 30 seconds!"
        timeout /t 25 /nobreak
        mcrcon -p passcode -w 1 "say 5" "say 4" "say 3" "say 2" "say 1"
    )
    mcrcon -p passcode -w 3 save-all stop
    taskkill py.exe
    taskkill python.exe
    del on.txt
    taskkill /f /im cmd.exe
)

goto stopcheck