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
        """Join in the current game

        !join"""
        await logging_utils.log_command("join", ctx.channel, ctx.author)
        if ctx.channel.id != discord_ids.LOBBY_CHANNEL_ID:
            await ctx.send(f"{ctx.author.mention} cannot join game from {ctx.channel.mention}. Head over "
                     f"to {ctx.guild.get_channel(discord_ids.LOBBY_CHANNEL_ID).mention} and use `{ctx.prefix}join` "
                     f"to play in today's LIVE game!")

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
                await ctx.author.add_roles(ctx.guild.get_role(discord_ids.CURRENT_PLAYER_ROLE_ID))
            await ctx.message.add_reaction(EMOJIS[":white_check_mark:"])
        # Error messages for having too few or too many houses/tiers
        else:
            await ctx.message.add_reaction(EMOJIS[":x:"])
            await ctx.send(f"{ctx.author.mention} Please make sure you have ONE house and ONE tier role before joining. "
                           f"You currently have {num_tier_roles} tier roles and {num_house_roles} house roles.")


def setup(bot):
    bot.add_cog(PlayerOpsCog(bot))
