::@echo off

mcrcon -p passcode -w 20 "say Manual shutdown initiated; server stopping in 20 seconds." stop
timeout /t 3 /nobreak

:: get current hour
for /f %%a in ('Powershell -Nop -c "Get-Date -Format 'HH'"') do set getcurrHour2=%%a
set /a "hour2=(1%getcurrhour2%-100)"

:: kill main.py
taskkill /f /im py.exe
taskkill /f /im python.exe
if %hour2% lss 23 if %hour2% gtr 8 (
    timeout /t 1 /nobreak
    start /min main.py
)

del on.txt
taskkill /f /im cmd.exe
taskkill /f /im cmd.exe
:: (twice for good measure)