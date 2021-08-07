from discord.ext import commands


def is_in_guild(guild_id):
    """Check that command is in a guild"""

    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id

    return commands.check(predicate)
