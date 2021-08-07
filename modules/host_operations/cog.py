from discord.ext import commands
from utils import logging_utils
import discord_ids
from datetime import datetime
import discord


class GameOpsCog(commands.Cog, name="Game Operations"):
    """Commands for Game Hosts to start and end dueling games"""
    def __init__(self, bot):
        self.bot = bot

    def get_roster(self, guild, role):
        """Gets all people from GUILD with ROLE, their HOUSE and TIER"""
        current_players = role.members
        roster = []
        for player in current_players:
            roster_entry = [player.nick if player.nick is not None else player.name, "", ""]
            for player_role in player.roles:
                if player_role.id in discord_ids.HOUSE_ROLES:
                    roster_entry[1] = guild.get_role(player_role.id).name
                elif player_role.id in discord_ids.TIER_ROLES:
                    roster_entry[2] = guild.get_role(player_role.id).name
            roster.append(",".join(roster_entry))
        return roster

    @commands.command(name="openlobby")
    @commands.has_permissions(administrator=True)
    async def openlobby(self, ctx):
        """Unlocks lobby, posts a welcome message like how to use !join, tag @TriviaTuesday

        !openlobby"""
        await logging_utils.log_command("openlobby", ctx.channel, ctx.author)
        lobby_channel = ctx.guild.get_channel(discord_ids.LOBBY_CHANNEL_ID)
        lock_perms = lobby_channel.overwrites_for(ctx.guild.default_role)
        lock_perms.send_messages = True
        await lobby_channel.set_permissions(ctx.guild.default_role, overwrite=lock_perms)
        await lobby_channel.send(f"It's {ctx.guild.get_role(discord_ids.TRIVIA_TUESDAY_ROLE_ID).mention},"
                                 f" and the Lobby is OPEN! {discord_ids.SNOO_SMILE_EMOJI} \n\n"
                                 f"Before we start, head to "
                                 f"{ctx.guild.get_channel(discord_ids.GAME_SIGNUPS_CHANNEL_ID).mention} "
                                 f"to verify your House and Tier! {discord_ids.TADA_EMOJI}\n\n"
                                 f"Then, when you're ready, use the command `!join` to play in today's LIVE game! "
                                 f"{discord_ids.HYPE_EMOJI}")

    @commands.command(name="startgame", aliases=["start"])
    @commands.has_permissions(administrator=True)
    async def startgame(self, ctx):
        """Sends a message on how to sign up for future game pings (i.e. @TriviaTuesday role)
        Locks the lobby,
        Posts a message in #gameplay with instructions
        Tag @CurrentPlayer to say the game is starting

        !startgame"""
        await logging_utils.log_command("startgame", ctx.channel, ctx.author)

        # Lock the lobby channel
        lobby_channel = ctx.guild.get_channel(discord_ids.LOBBY_CHANNEL_ID)
        lock_perms = lobby_channel.overwrites_for(ctx.guild.default_role)
        lock_perms.send_messages = False
        await lobby_channel.send(f"The {lobby_channel.mention} is now locked as this week's game is about to begin. Want to"
                                 f" sign up for future gametime announcement pings? Please see (uhhh, who? what? where?)"
                                 f" probably {ctx.guild.get_channel(discord_ids.GAME_SIGNUPS_CHANNEL_ID).mention}")
        await lobby_channel.set_permissions(ctx.guild.default_role, overwrite=lock_perms)

        # Post the roster
        roster = self.get_roster(ctx.guild, ctx.guild.get_role(discord_ids.CURRENT_PLAYER_ROLE_ID))
        roster = sorted(roster, key=lambda x: x.lower())
        # Ping CurrentPlayer in #gameplay
        gameplay_channel = ctx.guild.get_channel(discord_ids.GAMEPLAY_CHANNEL_ID)
        await gameplay_channel.send(f"{ctx.guild.get_role(discord_ids.CURRENT_PLAYER_ROLE_ID).mention} "
                                    f"The current game is set to begin!\n\n"
                                    f"The following players have signed up for today's LIVE game. If you see an error "
                                    f"or omission, please let today's host, {ctx.author.mention}, know as soon as possible:\n\n"
                                    f"{chr(10).join(roster)}")
        game_logs_channel = ctx.guild.get_channel(discord_ids.GAME_LOG_CHANNEL_ID)
        await game_logs_channel.send(chr(10).join(roster))

    @commands.command(name="endgame", alises=["end"])
    @commands.has_permissions(administrator=True)
    async def endgame(self, ctx):
        """Removes the CurrentPlayer role from everyone, announces the game has ended

        !endgame"""
        await logging_utils.log_command("endgame", ctx.channel, ctx.author)

        current_player_role = ctx.guild.get_role(discord_ids.CURRENT_PLAYER_ROLE_ID)
        for player in current_player_role.members:
            await player.remove_roles(current_player_role)

        announcements_channel = ctx.guild.get_channel(discord_ids.ANNOUNCEMENTS_CHANNEL_ID)
        embed = discord.Embed(title=f"{datetime.now().strftime('%B %d, %Y')} Dueling Game RESULTS",
                              description="Thank you to everyone who played! Today's dueling LIVE game has now ended. "
                                          "\n\n**RESULTS**? When will the home game be posted? Tonight? idk ")
        await announcements_channel.send(embed=embed)

    @commands.command(name="roster")
    @commands.has_permissions(administrator=True)
    async def roster(self, ctx):
        """Gets the roster of current players for today's LIVE game

        !roster"""
        # Print out the roster
        roster = self.get_roster(ctx.guild, ctx.guild.get_role(discord_ids.CURRENT_PLAYER_ROLE_ID))
        roster = sorted(roster, key=lambda x: x.lower())
        await ctx.send(chr(10).join(roster))


def setup(bot):
    bot.add_cog(GameOpsCog(bot))
