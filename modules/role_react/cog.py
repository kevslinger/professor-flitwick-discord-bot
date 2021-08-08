import discord
import json
from discord.ext import commands

import constants
import discord_ids
from utils import google_utils, logging_utils
from datetime import datetime


class RoleReactCog(commands.Cog, name="Role React"):
    """Set up a role react message where people can choose their own roles in the server"""
    def __init__(self, bot):
        self.bot = bot
        self.gspread_client = google_utils.create_gspread_client()
        self.rolereact_sheet = self.gspread_client.open_by_key(constants.GOOGLE_SHEET_KEY)\
            .worksheet(constants.ROLE_REACT_SHEET_NAME)

    @commands.command(name="rolereact")
    @commands.has_permissions(administrator=True)
    async def rolereact(self, ctx):
        """Set up an embed which has reactions to gain roles in the server. Only for admins

        Usage: `!rolereact`"""
        await logging_utils.log_command("rolereact", ctx.channel, ctx.author)
        # Creating, sending, logging in google sheets, and adding reacts for the HOUSE signup embed
        house_embed = discord.Embed(title="House Signups!",
                              description="Pick your house by reacting to this message!\n"
                                          "Note: You may only have **one** house at a time.\n"
                                          "To change tier, remove the reaction for your current tier and add the reaction "
                                          "for your new tier\n\n"
                                          f"{chr(10).join([f'{emoji}: <@&{role}>' for emoji, role in discord_ids.HOUSE_REACT_DICT.items()])}",
                              color=constants.EMBED_COLOR)
        house_msg = await ctx.send(embed=house_embed)
        # Add the message to our DB (google sheets) for combination with on_raw_reaction_add and on_raw_reaction_remove
        self.rolereact_sheet.append_row([datetime.now().strftime("%m/%d/%y %H:%M:%S"), ctx.guild.name, ctx.channel.name,
                                         f"{house_msg.id}", json.dumps(discord_ids.HOUSE_REACT_DICT)])
        # Add all the appropriate reactions to the message
        for emoji in discord_ids.HOUSE_REACT_DICT:
            await house_msg.add_reaction(emoji)
        # Creating, sending, logging in google sheets, and adding reacts for the TIER signup embed
        tier_embed = discord.Embed(title="Tier Signups!",
                              description="Pick your tier by reacting to this message!\n"
                                          "Note: You may only have **one** tier at a time.\n"
                                          "To change tier, remove the reaction for your current tier and add the reaction "
                                          "for your new tier\n\n"
                                          f"{chr(10).join([f'{emoji}: <@&{role}>' for emoji, role in discord_ids.TIER_REACT_DICT.items()])}",
                              color=constants.EMBED_COLOR)
        tier_msg = await ctx.send(embed=tier_embed)
        # Add the message to our DB (google sheets) for combination with on_raw_reaction_add and on_raw_reaction_remove
        self.rolereact_sheet.append_row(
            [datetime.now().strftime("%m/%d/%y %H:%M:%S"), ctx.guild.name, ctx.channel.name, f"{tier_msg.id}",
             json.dumps(discord_ids.TIER_REACT_DICT)])
        # Add all the appropriate reactions to the message
        for emoji in discord_ids.TIER_REACT_DICT:
            await tier_msg.add_reaction(emoji)
        # Creating, sending, logging in google sheets, and adding reacts for the TIER signup embed
        ping_embed = discord.Embed(title="Ping Signups!",
                              description=f"React with {discord_ids.CALENDAR_EMOTE} to get the "
                                          f"{ctx.guild.get_role(discord_ids.TRIVIA_TUESDAY_ROLE_ID).mention} role and "
                                          f"receive pings when each game is starting!",
                              color=constants.EMBED_COLOR)
        ping_msg = await ctx.send(embed=ping_embed)
        # Add the message to our DB (google sheets) for combination with on_raw_reaction_add and on_raw_reaction_remove
        self.rolereact_sheet.append_row(
            [datetime.now().strftime("%m/%d/%y %H:%M:%S"), ctx.guild.name, ctx.channel.name, f"{ping_msg.id}",
             json.dumps(discord_ids.PING_REACT_DICT)])
        # Add all the appropriate reactions to the message
        for emoji in discord_ids.PING_REACT_DICT:
            await ping_msg.add_reaction(emoji)
        # Delete the user's message just because lol
        await ctx.message.delete()


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Handle a reaction being added to the role react message"""
        #print(payload.emoji)
        #print(payload.event_type)
        # Don't do anything when we react to our own message
        if payload.user_id == discord_ids.BOT_USER_ID:
            #print("payload is user id")
            return

        # Makes sure the message reacted to is one of our role react messages
        result_cell = self.rolereact_sheet.find(f"{payload.message_id}", in_column=4)
        if result_cell is None:
            print(f"result cell is none")
            return

        # My plan for this part...
        # Should I look at the message, loop over all reactions, check the user that reacted. If it's the current user,
        # remove that reaction? How slow is that?
        # Shit I don't think I can do this.
        # I don't think I have access to the users who are on each reaction.
        # So maybe I should just keep it the way it is for now...I mean, it's fine.
        role_map = json.loads(self.rolereact_sheet.cell(result_cell.row, result_cell.col+1).value)
        if f"{payload.emoji}" in role_map:
            #channel = await self.bot.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(payload.message_id)
            #for reaction in channel.reactions:
            #    print(reaction)
            # Ah I have to hardcode everything anyways I think
            #if role_map[f"{payload.emoji}"] in discord_ids.HOUSE_ROLES and any([role.id == int(house_role) for role in payload.member.roles for house_role in discord_ids.HOUSE_ROLES]):
            #    await reaction.remove(user)
            #    return
            role = self.bot.get_guild(payload.guild_id).get_role(int(role_map[f"{payload.emoji}"]))
            await payload.member.add_roles(role)

            print(f"Gave the {role.name} role to {payload.member}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Handle a reaction being removed from the role react message"""
        # Makes sure the message reacted to is one of our role react messages
        result_cell = self.rolereact_sheet.find(f"{payload.message_id}", in_column=4)
        if result_cell is None:
            return

        role_map = json.loads(self.rolereact_sheet.cell(result_cell.row, result_cell.col+1).value)
        if f"{payload.emoji}" in role_map:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(int(role_map[f"{payload.emoji}"]))
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)

            print(f"Removed the {role.name} role from {member}")


def setup(bot):
    bot.add_cog(RoleReactCog(bot))
