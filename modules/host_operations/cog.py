from discord.ext import commands
from utils import logging_utils
from modules.host_operations import host_operations_constants
from datetime import datetime
import discord


class GameOpsCog(commands.Cog, name="Game Operations"):
    """Commands for Game Hosts to start and end dueling games"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="openlobby")
    @commands.has_permissions(administrator=True)
    async def openlobby(self, ctx):
        """Unlocks lobby, posts a welcome message like how to use !join, tag @TriviaTuesday"""
        logging_utils.log_command("openlobby", ctx.channel, ctx.author)
        lobby_channel = ctx.guild.get_channel(host_operations_constants.LOBBY_CHANNEL_ID)
        lock_perms = lobby_channel.overwrites_for(ctx.guild.default_role)
        lock_perms.send_messages = True
        await lobby_channel.set_permissions(ctx.guild.default_role, overwrite=lock_perms)
        await lobby_channel.send(f"It's {ctx.guild.get_role(host_operations_constants.TRIVIA_TUESDAY_ROLE_ID).mention}, "
                                 f"and the Lobby is OPEN! <:gottaGo:839282914051227649>\n\n"
                                 f"Before we start, head to {ctx.guild.get_channel(host_operations_constants.GAME_SIGNUPS_CHANNEL_ID).mention} "
                                 f"to verify your House and Tier! <:thumbnail:842965702288998400>\n\n"
                                 f"Then, when you're ready, use the command `!join` to play in today's LIVE game! <:angryGeno:842965440619610124>")

    @commands.command(name="startgame", aliases=["start"])
    @commands.has_permissions(administrator=True)
    async def startgame(self, ctx):
        """Sends a message on how to sign up for future game pings (i.e. @TriviaTuesday role)
        Locks the lobby,
        Posts a message in #gameplay with instructions
        Tag @CurrentPlayer to say the game is starting"""
        logging_utils.log_command("startgame", ctx.channel, ctx.author)

        # Lock the lobby channel
        lobby_channel = ctx.guild.get_channel(host_operations_constants.LOBBY_CHANNEL_ID)
        lock_perms = lobby_channel.overwrites_for(ctx.guild.default_role)
        lock_perms.send_messages = False
        await lobby_channel.set_permissions(ctx.guild.default_role, overwrite=lock_perms)
        await lobby_channel.send(f"The {lobby_channel.mention} is now locked as today's game is about to begin. Want to"
                                 f" sign up for future gametime announcement pings? Please see (uhhh, who? what? where?)")

        # Ping CurrentPlayer in #gameplay
        gameplay_channel = ctx.guild.get_channel(host_operations_constants.GAMEPLAY_CHANNEL_ID)
        await gameplay_channel.send(f"{ctx.guild.get_role(host_operations_constants.CURRENT_PLAYER_ROLE_ID).mention} The current game is set to begin!\n\n"
                                    f"I should probably tell you how discord dueling works but honestly I don't even know, so\n\n"
                                    f"Please wait for today's host, {ctx.author.mention} to give the first question!")

    @commands.command(name="endgame", alises=["end"])
    @commands.has_permissions(administrator=True)
    async def endgame(self, ctx):
        "Removes the CurrentPlayer role from everyone, announces the game has ended"
        logging_utils.log_command("endgame", ctx.channel, ctx.author)

        current_player_role = ctx.guild.get_role(host_operations_constants.CURRENT_PLAYER_ROLE_ID)
        for player in current_player_role.members:
            await player.remove_roles(current_player_role)

        announcements_channel = ctx.guild.get_channel(host_operations_constants.ANNOUNCEMENTS_CHANNEL_ID)
        embed = discord.Embed(title=f"{datetime.now().strftime('%B %d, %Y')} Dueling Game RESULTS",
                              description="Thank you to everyone who played! Today's dueling LIVE game has now ended. \n\n"
                                         "**RESULTS**? When will the home game be posted? Tonight? idk ")
        await announcements_channel.send(embed=embed)



def setup(bot):
    bot.add_cog(GameOpsCog(bot))