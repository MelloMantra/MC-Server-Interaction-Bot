@echo off

:: wait for server to start
timeout /t 6 /nobreak

::mcrcon -p passcode "scoreboard objectives add players dummy"
set uptime = 0

:stopcheck

:: wait 10 minutes
cls
echo Uptime: Approx. %uptime% minutes.
timeout /t 300 /nobreak
set /a uptime = %uptime%+5

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
    del on.txt
)

:: time-based shutdown
if %hour% gtr 22 (
    if not %playercount%==d (
        mcrcon -p passcode "title @a actionbar "The server is shutting down for the day in 30 seconds!""
        timeout /t 25 /nobreak
        mcrcon -p passcode -w 1 "say 5" "say 4" "say 3" "say 2" "say 1"
    )
    mcrcon -p passcode -w 3 save-all stop
    del on.txt
)

:: close if server off
if not exist on.txt (
    echo Server stopped (automatically) on %date% at %time%
    exit
)

goto stopcheck
