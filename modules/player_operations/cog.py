import discord
from discord.ext import commands

import discord_ids
from utils import logging_utils
from emoji import EMOJI_ALIAS_UNICODE_ENGLISH as EMOJIS


class PlayerOpsCog(commands.Cog, name="Player Operations"):
    """Commands for players to use (e.g. join in games)"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join")
    async def join(self, ctx):
        """Join in the current game. Must have one HOUSE role and one TIER role to join.

        Usage: `!join`"""
        await logging_utils.log_command("join", ctx.channel, ctx.author)
        # Players can only join within the lobby. This is to ensure you can only signup after the host has
        # Used !openlobby, and people won't be able to sneak in the currentPlayer role overnight
        if ctx.channel.id != discord_ids.LOBBY_CHANNEL_ID:
            await ctx.message.add_reaction(EMOJIS[":x:"])
            await ctx.send(f"{ctx.author.mention} cannot join game from {ctx.channel.mention}. Head over "
                     f"to {ctx.guild.get_channel(discord_ids.LOBBY_CHANNEL_ID).mention} and use `{ctx.prefix}join` "
                     f"to play in today's LIVE game!")
            return

        # The live games are capped at (20?) players
        # TODO: Check what the player cap should be. Talks of increasing it?
        player_cap = 25
        current_player_role = ctx.guild.get_role(discord_ids.CURRENT_PLAYER_ROLE_ID)
        if len(current_player_role.members) >= player_cap:
            await ctx.message.add_reaction(EMOJIS[":x:"])
            await ctx.send(f"Sorry {ctx.author.mention}, we're already at full capacity for this week's LIVE game. "
                           f"You can still play the HOME game later via google forms. Don't forget to pick up the "
                           f"{ctx.guild.get_role(discord_ids.TRIVIA_TUESDAY_ROLE_ID).name} role in "
                           f"{ctx.guild.get_channel(discord_ids.GAME_SIGNUPS_CHANNEL_ID).mention} to be alerted the "
                           f"next time a LIVE game is open!")
            return

        num_house_roles = 0
        num_tier_roles = 0
        for role in ctx.author.roles:
            if role.id in discord_ids.HOUSE_ROLES:
                num_house_roles += 1
            if role.id in discord_ids.TIER_ROLES:
                num_tier_roles += 1
        # If the player has exactly one house and exactly one tier, give them the current player role.
        if num_house_roles == 1 and num_tier_roles == 1:
            if discord_ids.CURRENT_PLAYER_ROLE_ID not in [role.id for role in ctx.author.roles]:
                await ctx.author.add_roles(current_player_role)
            await ctx.message.add_reaction(EMOJIS[":white_check_mark:"])
        # Error messages for having too few or too many houses/tiers
        else:
            await ctx.message.add_reaction(EMOJIS[":x:"])
            await ctx.send(f"{ctx.author.mention} Please make sure you have ONE house and ONE tier role before joining. "
                           f"You currently have {num_tier_roles} tier roles and {num_house_roles} house roles.")

    @commands.command(name="unjoin")
    async def unjoin(self, ctx):
        """Unregister yourself. Can only be done **before** the LIVE game starts

        Usage: `!unjoin`"""
        await logging_utils.log_command("join", ctx.channel, ctx.author)
        if ctx.channel.id != discord_ids.LOBBY_CHANNEL_ID:
            await ctx.send(f"{ctx.author.mention} cannot unjoin game from {ctx.channel.mention}. Head over to "
                           f"{ctx.guild.get_channel(discord_ids.LOBBY_CHANNEL_ID).mention} and use `{ctx.prefix}unjoin`"
                           f" to unenroll in the current game. If the LIVE game has already started, you cannot unjoin.")
            await ctx.message.add_reaction(EMOJIS[":x:"])
            return
        await ctx.author.remove_roles(ctx.guild.get_role(discord_ids.CURRENT_PLAYER_ROLE_ID))
        await ctx.message.add_reaction(EMOJIS[":white_check_mark:"])

    @commands.command(name="msghost")
    @commands.has_any_role(
        discord_ids.CURRENT_PLAYER_ROLE_ID,
    )
    async def msghost(self, ctx):
        """Opens a channel in the gameplay category which lets the player talk to the host

        Usage: `!msghost`"""
        await logging_utils.log_command("msghost", ctx.channel, ctx.author)

        if ctx.channel.id != discord_ids.GAMEPLAY_CHANNEL_ID and ctx.channel.id != discord_ids.LOBBY_CHANNEL_ID:
            await ctx.send(f"{ctx.author.mention} cannot open host channel here. Please use `{ctx.prefix}msghost` in "
                           f"either the {ctx.guild.get_channel(discord_ids.GAMEPLAY_CHANNEL_ID).mention} or "
                           f"{ctx.guild.get_channel(discord_ids.LOBBY_CHANNEL_ID).mention}.")
            return

        try:
            new_channel = await ctx.guild.create_text_channel(f"{ctx.author.nick if ctx.author.nick is not None else ctx.author.name}",
                                                              category=ctx.channel.category,
                                                              overwrites={
                                                                  ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                                                  ctx.author: discord.PermissionOverwrite(read_messages=True,
                                                                                                          send_messages=True)})
        except discord.Forbidden:
            await ctx.guild.get_channel(discord_ids.BOT_LOG_CHANNEL_ID).send(f"ACCESS DENIED: Could not create channel "
                                                                             f"for {ctx.author.name} to speak to host.")


def setup(bot):
    bot.add_cog(PlayerOpsCog(bot))
