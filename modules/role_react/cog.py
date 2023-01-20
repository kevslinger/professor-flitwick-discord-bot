import discord
import json
from discord.ext import commands

import constants
import discord_ids
from utils import google_utils, logging_utils
from datetime import datetime
import asyncio


class RoleReactCog(commands.Cog, name="Role React"):
    """Set up a role react message where people can choose their own roles in the server"""

    def __init__(self, bot):
        self.bot = bot
        self.gspread_client = google_utils.create_gspread_client()
        self.rolereact_sheet = self.gspread_client.open_by_key(
            constants.GOOGLE_SHEET_KEY
        ).worksheet(constants.ROLE_REACT_SHEET_NAME)
        self.lock = asyncio.Lock()

    @commands.command(name="rolereact")
    @commands.has_permissions(administrator=True)
    async def rolereact(self, ctx):
        """Set up an embed which has reactions to gain roles in the server. Only for admins

        Usage: `!rolereact`"""
        await logging_utils.log_command("rolereact", ctx.channel, ctx.author)
        # Creating, sending, logging in google sheets, and adding reacts for the HOUSE signup embed
        house_embed = discord.Embed(
            title="House Signups!",
            description="Pick your house by reacting to this message!\n"
            "Note: You may only have **one** house at a time.\n"
            "To change tier, remove the reaction for your current tier and add the reaction "
            "for your new tier\n\n"
            f"{chr(10).join([f'{emoji}: <@&{role}>' for emoji, role in discord_ids.HOUSE_REACT_DICT.items()])}",
            color=constants.EMBED_COLOR,
        )
        house_msg = await ctx.send(embed=house_embed)
        # Add the message to our DB (google sheets) for combination with on_raw_reaction_add and on_raw_reaction_remove
        self.rolereact_sheet.append_row(
            [
                datetime.now().strftime("%m/%d/%y %H:%M:%S"),
                ctx.guild.name,
                ctx.channel.name,
                f"{house_msg.id}",
                json.dumps(discord_ids.HOUSE_REACT_DICT),
            ]
        )
        # Add all the appropriate reactions to the message
        for emoji in discord_ids.HOUSE_REACT_DICT:
            await house_msg.add_reaction(emoji)
        # Creating, sending, logging in google sheets, and adding reacts for the TIER signup embed
        tier_embed = discord.Embed(
            title="Tier Signups!",
            description="Pick your tier by reacting to this message!\n"
            "Note: You may only have **one** tier at a time.\n"
            "To change tier, remove the reaction for your current tier and add the reaction "
            "for your new tier\n\n"
            f"{chr(10).join([f'{emoji}: <@&{role}>' for emoji, role in discord_ids.TIER_REACT_DICT.items()])}",
            color=constants.EMBED_COLOR,
        )
        tier_msg = await ctx.send(embed=tier_embed)
        # Add the message to our DB (google sheets) for combination with on_raw_reaction_add and on_raw_reaction_remove
        self.rolereact_sheet.append_row(
            [
                datetime.now().strftime("%m/%d/%y %H:%M:%S"),
                ctx.guild.name,
                ctx.channel.name,
                f"{tier_msg.id}",
                json.dumps(discord_ids.TIER_REACT_DICT),
            ]
        )
        # Add all the appropriate reactions to the message
        for emoji in discord_ids.TIER_REACT_DICT:
            await tier_msg.add_reaction(emoji)
        # Creating, sending, logging in google sheets, and adding reacts for the TIER signup embed
        ping_embed = discord.Embed(
            title="Ping Signups!",
            description=f"React with {discord_ids.CALENDAR_EMOTE} to get the "
            f"{ctx.guild.get_role(discord_ids.TRIVIA_TUESDAY_ROLE_ID).mention} role and "
            f"receive pings when each game is starting!",
            color=constants.EMBED_COLOR,
        )
        ping_msg = await ctx.send(embed=ping_embed)
        # Add the message to our DB (google sheets) for combination with on_raw_reaction_add and on_raw_reaction_remove
        self.rolereact_sheet.append_row(
            [
                datetime.now().strftime("%m/%d/%y %H:%M:%S"),
                ctx.guild.name,
                ctx.channel.name,
                f"{ping_msg.id}",
                json.dumps(discord_ids.PING_REACT_DICT),
            ]
        )
        # Add all the appropriate reactions to the message
        for emoji in discord_ids.PING_REACT_DICT:
            await ping_msg.add_reaction(emoji)
        # Delete the user's message just because lol
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Handle a reaction being added to the role react message"""
        # Don't do anything when we react to our own message
        if payload.user_id == discord_ids.BOT_USER_ID:
            return

        # Makes sure the message reacted to is one of our role react messages
        result_cell = self.rolereact_sheet.find(f"{payload.message_id}", in_column=4)
        if result_cell is None:
            return

        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        member = guild.get_member(payload.user_id)
        reaction = str(payload.emoji)
        # Gets the dictionary which maps reactions to roles from the google sheet.
        role_map = json.loads(
            self.rolereact_sheet.cell(result_cell.row, result_cell.col + 1).value
        )
        # Without a lock, the behavior when the user selects multiple reactions quickly is weird.
        async with self.lock:
            # Check if the reaction is one of the valid ones to give role. If not, just remove the reaction
            # and we're done.
            if reaction in role_map:
                # At this point, we know the user has selected a valid emoji to pick up a role.
                # We need to loop over the roles in the role map, remove all the others if the user has them,
                # remove those reactions, and then assign the role
                role_ids = [role.id for role in member.roles]
                # Get the role-react message from the channel
                # TODO: Does this need to be in the lock?
                message = await channel.fetch_message(payload.message_id)
                # Loop over all the possible reacts and roles. If the user has a role other than the one being
                # reacted to, remove that reaction.
                # TODO: Should we loop over reactions here? I don't think so
                for emoji, role_id in role_map.items():
                    if role_id in role_ids and role_id != role_map[reaction]:
                        # NOTE: When we remove the reaction, on_raw_reaction_remove get triggered
                        # and will remove the role. Pretty nifty.
                        await message.remove_reaction(emoji, member)

                role = guild.get_role(int(role_map[reaction]))
                await member.add_roles(role)
                print(f"Gave the {role.name} role to {member}")
            else:
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(reaction, member)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Handle a reaction being removed from the role react message"""
        # Makes sure the message reacted to is one of our role react messages
        result_cell = self.rolereact_sheet.find(f"{payload.message_id}", in_column=4)
        if result_cell is None:
            return
        # Get the dictionary which maps reactions to roles.
        role_map = json.loads(
            self.rolereact_sheet.cell(result_cell.row, result_cell.col + 1).value
        )
        if f"{payload.emoji}" in role_map:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(int(role_map[f"{payload.emoji}"]))
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)

            print(f"Removed the {role.name} role from {member}")


def setup(bot):
    bot.add_cog(RoleReactCog(bot))
