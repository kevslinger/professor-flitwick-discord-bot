import discord
import json
from discord.ext import commands

import constants
from utils import google_utils, logging_utils
from modules.role_react import role_react_constants

class RoleReactCog(commands.Cog, name="Role React"):
    """Set up a role react"""
    def __init__(self, bot):
        self.bot = bot
        self.gspread_client = google_utils.create_gspread_client()
        self.rolereact_sheet = self.gspread_client.open_by_key("1Uk_YGKbgbnJZQn6__he3jdIOamB-1Ytm4i1-v_eDC0U").sheet1

    @commands.command(name="rolereact")
    @commands.has_permissions(administrator=True)
    async def rolereact(self, ctx):
        """Set up an embed which has reactions to gain roles in the server"""
        logging_utils.log_command("rolereact", ctx.channel, ctx.author)
        embed = discord.Embed(title="House and Tier signups!",
                              description="Pick your house and tier by reacting to this message!\n"
                                          "Note: You may only have **one** house and **one** tier at a time.\n"
                                          "To remove a role, simply remove the reaction.\n\n**HOUSES**\n"
                                          f"{chr(10).join([f'{emoji}: <@&{role}>' for emoji, role in role_react_constants.ROLE_REACT_DICT1.items()])}\n\n"
                                          f"**TIERS**\n"
                                          f"{chr(10).join([f'{emoji}: <@&{role}>' for emoji, role in role_react_constants.ROLE_REACT_DICT2.items()])}")
        msg = await ctx.send(embed=embed)
        for emoji in {**role_react_constants.ROLE_REACT_DICT1, **role_react_constants.ROLE_REACT_DICT2}:
            await msg.add_reaction(emoji)

        self.rolereact_sheet.append_row([ctx.guild.name, ctx.channel.name, f"{msg.id}", json.dumps({**role_react_constants.ROLE_REACT_DICT1, **role_react_constants.ROLE_REACT_DICT2})])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Handle a reaction being added to the role react message"""
        print(payload.emoji)
        # Don't do anything when we react to our own message
        if payload.user_id == constants.BOT_USER_ID:
            print("payload is user id")
            return

        # Makes sure the message reacted to is one of our role react messages
        result_cell = self.rolereact_sheet.find(f"{payload.message_id}", in_column=3)
        if result_cell is None:
            print(f"result cell is none")
            return

        role_map = json.loads(self.rolereact_sheet.cell(result_cell.row, result_cell.col+1).value)
        if f"{payload.emoji}" in role_map:
            # Ah fuck I have to hardcode everything anyways I think
            if role_map[f"{payload.emoji}"] in role_react_constants.HOUSE_ROLES and any([role.id == int(house_role) for role in payload.member.roles for house_role in role_react_constants.HOUSE_ROLES]):
                await reaction.remove(user)
                return
            if role_map[f"{payload.emoji}"] in role_react_constants.TIER_ROLES and any([role.id == int(tier_role) for role in payload.member.roles for tier_role in role_react_constants.TIER_ROLES]):
                # TODO: how to deal with no longer having reaction here.
                await reaction.remove(payload.member)
                return
            await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(int(role_map[f"{payload.emoji}"])))


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Handle a reaction being removed from the role react message"""
        print(payload.emoji)
        # Makes sure the message reacted to is one of our role react messages
        result_cell = self.rolereact_sheet.find(f"{payload.message_id}", in_column=3)
        if result_cell is None:
            return

        role_map = json.loads(self.rolereact_sheet.cell(result_cell.row, result_cell.col+1).value)
        if f"{payload.emoji}" in role_map:
            # Ah fuck I have to hardcode everything anyways I think

            await payload.member.remove_roles(self.bot.get_guild(payload.guild_id).get_role(int(role_map[f"{reaction.emoji}"])))

def setup(bot):
    bot.add_cog(RoleReactCog(bot))