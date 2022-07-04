@echo off
set RAM=4

:: start server
cd "C:\Users\mgdr0\Desktop\Misc\Minecraft Server"
java -Xmx%RAM%G -Xms%RAM%G -jar server.jar