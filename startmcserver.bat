@echo off
title "Server CLI"
set RAM=4

:: start server
cd "C:\Users\mgdr0\Desktop\Misc\Minecraft Server"
java -Xmx%RAM%G -Xms%RAM%G -jar server.jar

:loop

:: detect if server off
tasklist |findstr /ibc:"java.exe" || (
    del on.txt
    exit
)

goto loop