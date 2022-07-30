@echo off

:loop

:: detect if server off
tasklist |findstr /ibc:"java.exe" || del on.txt

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