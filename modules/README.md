# Professor Flitwick Discord Bot Command Modules

Professor Flitwick is composed of several independent modules.
Each module has a set of one or more related commands.

# Help Module

The Help module enables users to use the `help` command, which will display all commands available to them.
This module was adapated from (with minimal modification) DenverCoder1's Help module in his [Weasley Chess bot](https://github.com/DenverCoder1/weasley-chess-bot).

# Host Operations Module

The Host Operations module contains the commands for the dueling host to use during a live game. 
Namely, the commands included in this module are:

- `openlobby`: Unlocks the lobby channel, posts a welcome message, and pings the `TriviaTuesday` discord role to let them know a new game is about to begin.
- `startgame`: Locks the lobby channel, pings the `CurrentPlayer` role to announce the game is aboug to begin. Then prints out the roster to the `game-logs` channel.
- `endgame`: Removes the `CurrentPlayer` role from everyone, announces the game has ended in the lobby and welcome channels.
- `roster`: Prints out the roster of the current players for the current live game.

# Player Operations Module

The Player Operations module contains the commands for the players to use to to join or unjoin live games, or to message the host while the game is going.
Namely, the commands include:

- `join`: Players that have exactly one house role and one tier role can use this to join the live game. Must do so in the lobby channel.
- `unjoin`: Used to unjoin the live game before it starts. Must do so in lobby channel.
- `msghost`: Use this in the lobby or gameplay channels to open up a new channel with just the player and host to allow the player to ask questions.

# Reddit Feed Module

The Reddit Feed module mainly deals with listening to r/Dueling and crossposting to the Announcements channel on discord. 
We take advantage of `discord.py`'s `@loop` decorator in the `reddit_feed` function to check for new posts/comments every 5 seconds. 
There is one command, namely:

- `resend`: This resends the most recent post in r/Dueling. It is not intended to be used unless the bot has a bug with it's listening loop.

# Role React Module

The Role React module enables players to react to a message to choose their house and tier roles.
The `role_react_constants.py` file has a set of Discord IDs for the emojis used in the role react message.
Most of this module uses the `Cog.listener` decorator to listen for react add/remove events in the server.
When a user reacts or removes a reaction from the role-react message in the `#game-signups` channel, the bot finds the role associated with that role, and accordingly adds or removes it from the player.
We maintain a google sheet which identifies the ID fo the role-react post as well as the mapping of react ID to role ID.
To create the role-react message, a mod can use the `rolereact` command, which should only be used if the original role-react message is deleted or became stale (i.e. the google sheet entry is deleted).
