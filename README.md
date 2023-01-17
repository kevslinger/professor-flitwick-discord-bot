# Professor Flitwick Discord Bot

Welcome to the documentation for the Professor Flitwick Discord Bot!
This bot was designed for the Harry Potter trivia competition hosted on https://www.reddit.com/r/dueling to host live trivia games on Discord.

# Table of Contents
- [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Installing Professor Flitwick](#installing-professor-flitwork)
    - [Google Cloud Account](#google-cloud-account)

# Installation

## Prerequisites

- [Python3.8 or newer](https://realpython.com/installing-python/)
- [Git](https://github.com/git-guides/install-git)
- [Pip package manager](https://phoenixnap.com/kb/install-pip-windows)

## Installing Professor Flitwork

We recommend using [virtual environments](https://docs.python.org/3/tutorial/venv.html) to manage python packages for this repo. 
To clone the repo and install dependencies, run the following on the command line

```bash
git clone git@github.com:kevslinger/professor-flitwick-discord-bot.git
cd professor-flitwick-discord-bot
virtualenv venv -p=3.8
pip install -r requirements.txt
```

These commands will copy this repository to your computer, set up the virtual environment, and install the required python packages in order to run the code.


## Google Cloud Account

TODO


## Env File

TODO

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
