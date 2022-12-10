# Minecraft Server Uptime Manager
A tool for managing your Minecraft server's uptime. Written mostly in Python, with several batch helper files. Currently a personal project only.

## Introduction
This project. This **stupid, bug infested project.**
I started this around the end of June, 2022, and still am not finished working out all of the bugs. Insects aside, I have established two methods for using this package.

## Method 1: Using the bot
**This method is recommended under all circumstances,** however, it only works for my own personal use (because I haven't coded in the ability to change directories based on the user, and other customization stuff). This method allows for users to execute  commands to interact with the Minecraft server (plus "ping" which is basically mandatory lol). If you really want to try to use the bot right now, you can click [here.](https://discord.com/api/oauth2/authorize?client_id=1003532411356844142&permissions=8&scope=bot%20applications.commands)

#### Default Prefix: **`.`**

#### Commands:
- `ping`............Pings the bot, bot responds with "pongers"
- `mcstart`.........Requests to start the server, bot responds with server status
- `mckill`..........Requests to stop the server (admin only), bot responds with server status

## Method 2: Using the Discord gateway filtration system **(BETA)**
**This method is dumb, stupid, bad, and braindead, why would anyone ever use it.**

...

Ok fine there is one practical use for it. If you would like to trigger the system via DMs or a group chat and/or any Discord server without inviting a bot. PLEASE NOTE that this method can recieve a command from **anywhere on Discord.** What I mean by that is that this method sifts through every single message you recieve, whether that be DMs, server messages, and even servers that you have muted or have notifications on "@mentions only". Also note that **this is a Beta version.** This system will be prone to bugs, crashes, and overall jankiness while I figure out how to make it run smoothly. But until then, just use the damn bot, it's so much simpler.

*External user compatibility coming soon!*

## Updates on progress:
- **Method 2** is now working (almost) flawlessly, but there are still some optimizations to be made.
- The bot is getting worked on daily, and I will continue to add new features to my heart's content.
- I have not pushed any changes to the repo in the past 2 weeks, but i will as soon as possible.
- I still have not made any progress on external user compatibility yet.
