# Professor Flitwick Discord Bot

Welcome to the documentation for the Professor Flitwick Discord Bot!
This bot was designed for the Harry Potter trivia competition hosted on https://www.reddit.com/r/dueling to host live trivia games on Discord.

# Table of Contents
- [Professor Flitwick Discord Bot](#professor-flitwick-discord-bot)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installing Professor Flitwork](#installing-professor-flitwork)
  - [Discord Developer Portal](#discord-developer-portal)
  - [Reddit Developer API](#reddit-developer-api)
  - [Google Cloud Account](#google-cloud-account)
  - [Env File](#env-file)
- [File Structure](#file-structure)
- [Hosting](#hosting)

# Installation

## Prerequisites

- [Git](https://github.com/git-guides/install-git)
- [Python3.8 or newer](https://realpython.com/installing-python/)
- [Pip package manager](https://phoenixnap.com/kb/install-pip-windows)

## Installing Professor Flitwork

We recommend using [virtual environments](https://virtualenv.pypa.io/en/latest/installation.html) to manage python packages for this repo.
Virtual environments allow you to configure the python packages for this repository independent of other packages installed on your computer.
Follow the link above to install `venv` on your computer. 
Then, in order to clone the repo and install dependencies, run the following on the command line

```bash
git clone git@github.com:kevslinger/professor-flitwick-discord-bot.git
cd professor-flitwick-discord-bot
virtualenv venv -p=3.8
pip install -r requirements.txt
```

These commands will first copy this repository to your computer, then set up the virtual environment, and finally install the required python packages in order to run the code.

## Discord Developer Portal

To create a Discord bot, you need to login to the [Discord Developer Portal](https://discord.com/developers/docs/intro). 
Once there, you can follow [this tutorial](https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/).
Professor Flitwick uses the `Manage Roles`, `Manage Channels`, `Manage Emojis and Stickers`, `Read Messages/View Channels`, `Send Messages`, `Embed Links`, `Read Message History`, and `Add Reactions` permissions.
The developer portal will have a Discord Token for the bot, which is required in the `.env` file.

## Reddit Developer API

Professor Flitwick listens to [r/Dueling](https://www.reddit.com/r/Dueling) and posts announcements to the Dueling Discord server.
In order to do this, a reddit account needs to be created with an app from the Reddit developer API.
Apps can be created [here](https://www.reddit.com/prefs/apps).
Name the app whatever you like, and choose `Script for personal use`.

## Google Cloud Account

Professor Flitwick uses a google sheet to maintain mappings from emotes to roles for the `game-signups` channel in the Dueling server.
To set that up, we need a google cloud account with a project that has activated the google sheets/drive APIs.
Once that has been created, the `client_secret.json` file in the project will have the information needed in the `.env` file.
Google Cloud is relatively hard to navigate. 
The following tutorials may help: [Official Doc](https://developers.google.com/maps/documentation/javascript/cloud-setup), [Unofficial Tutorial](https://www.balbooa.com/gridbox-documentation/how-to-get-google-client-id-and-client-secret).
This functionality is not mission critical to Professor Flitwick's operation.

## Env File

This bot uses a hidden `.env` file which holds sensitive information such as API keys (for Discord, Reddit, and Google Sheets). 
The file `.env.template` holds the variable names used by the rest of the bot.
Copy the `.env.template` file to `.env` and fill in the information.
**Do not publish `.env` publicly**

# File Structure

- [modules](./modules/) is a directory containing the python modules that store the bot's commands. Each module contains one or more commands for people to use within the discord server
- [utils](./utils/) contains utility python files to help with various services, such as Discord, Google Sheets, and Reddit.
- [.gitignore](./.gitignore) is a git-specific file for quality of life when using git's version control. It tells git which files not to keep track of, such as log and output files.
- [bot.py](./bot.py) is the python file we run to start the bot. It loads all the other bot modules from the [modules](./modules/) directory and listens to commands.
- [constants.py](./constants.py) is a python file that stores constant values for the bot.
- [discord_ids.py](./discord_ids.py) is a python file containing discord IDs for various emojis and roles within the Dueling Discord server.
- [LICENSE](./LICENSE) is the open source license for this project.
- [Procfile](./Procfile) is a Heroku-specific file which tells Heroku what to run to start the bot.
- [README.md](./README.md) documents how to use and install the bot.
- [requirements.txt](./requirements.txt) is a python-specific file which specifies the dependencies required to run this bot.
- [runtime.txt](./runtime.txt) a Heroku-specific file which specifies which version of python needs to be installed.

# Hosting

Currently, the bot is hosted on [Heroku](https://www.heroku.com). 
However, in 2022, Heroku announced the [removal of their free tier](https://blog.heroku.com/next-chapter), therefore ending its viability as a platform for this bot.
Professor Flitwick can use any standard hosting service (like a VPC).
At the bare minimum, it need only run on days in which a live game is happening for use of the `openlobby`, `startgame`, and `endgame` commands.
This would eliminate the effectiveness of the `reddit_feed` and `role_react` modules, but would preserve most of the functionality of the bot.
