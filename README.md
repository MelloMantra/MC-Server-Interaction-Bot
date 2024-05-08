# Minecraft Server Interaction Bot
A Discord bot named Tiko, written in Python by Mello Mantra. Tiko allows Discord users to interact with a Minecraft server via Discord commands. The purpose of this repository is to display a framework for such a bot, so directory navigation and such may not work as intended when directly ported to another system. If you decide to use this code, feel free to make edits on your own copy to make it work for your system. In my case, Tiko currently runs in all his glory on a Raspberry Pi 4 (4GB) running Raspbian Linux.

## Introduction
This bot allows users in the same guild as the bot to start a Minecraft server (if not already running) and query the status of the server. An administrator (designated by setting the `OWNER` variable in `configs.py` to the desired user's user ID) may use commands that can stop, forcefully stop, sleep, and wake the Minecraft server. The default prefix is `.`. Additionally, Tiko manages the uptime of your Minecraft server by turning it off automatically after 5 minutes of inactivity. Additionally, Tiko automatically restarts himself every ~24 hours.

## Dependencies
For this bot to run, the following Python libraries must be installed:

- `pycord`
- `mctools`
- `asyncio`
- `public_ip`
- `platform`
- `datetime`

## Usage
Listed below are the commands that can be issued followed by their function.

#### Minecraft Server Commands
- `.mc <option>` - Query the status of the Minecraft server. Returns status, version, and IP address with no arguments. The `/a` option appends the seed, world style, difficulty, allocated RAM, latency, and online players of the server. The `/b` option replaces the original status message with a brief, one line summary, displaying status and player count.
- `.start` - Starts the Minecraft server, unless already online or asleep.
- *`.stop` - Stops the Minecraft server, unless already off.
- *`.kill <option>` - The `option` is required. With the `/f` option, forcefully stops the Minecraft server, unless already off. With the `/s` option, it forcefully stops the Minecraft server and puts it into sleep mode, unless already asleep. Sleep mode prevents the `.start` and `.stop` commands from functioning. When this command is used with the `/w` option, the server is awakened from its slumber, unless already awake.
- *`.cli "<argument>"` - Executes `argument` on the Minecraft server command line (unless offline). Arguments with spaces must be enclosed in double quotes.
- *`.world <option>` - Non-functioning command to swap between world files. **WIP**.
- *`.motd "<argument>"` - Sets the Minecraft server MOTD to `argument`. Arguments with spaces must be enclosed in double quotes.
- *`.log <x>` - Displays the last `x` lines of the Minecraft server log file.

#### Other Commands
- `.ping` - Pings the bot and returns latency.
- *`.push` - Pushes all current changes to the connected GitHub repository. This is rarely used.
- *`.pull` - Pulls all updated files from the connected GitHub repository and overwrites existing files, except for the log file.

*Administrator privileges required

## Notes
The `tiko.desktop` and `tiko.service` files are here for users that would like to implement this on a Raspberry Pi like I did. There are instructions commented inside the files on what to do with each one.

:)
