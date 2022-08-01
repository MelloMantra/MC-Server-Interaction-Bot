@echo off
title "Maintainer"

set uptime = 0

:loop

:: timer increment
timeout /t 1 /nobreak
set /a uptime = %uptime%+1
echo Listener uptime: %uptime%
if %uptime% gtr 600 (
    set /a uptime = 0
    taskkill /f /im py.exe
    taskkill /f /im python.exe
    timeout /t 5 /nobreak
    goto restart
)

:: get current hour
for /f %%a in ('Powershell -Nop -c "Get-Date -Format 'HH'"') do set getcurrHour=%%a
set /a "hour=(1%getcurrhour%-100)"

:: test if detecting messages
if %hour% lss 23 if %hour% gtr 8 (
    tasklist |findstr /ibc:"py.exe" || goto restart
) else (
    taskkill /f /im py.exe
    taskkill /f /im python.exe
    exit
)

goto loop

:restart
start /min main.py
exit