from discord.ext import commands


def is_in_guild(guild_id):
    """Check that command is in a guild

    Args:
        guild_id: int, the specific guild's unique ID
    """

    # This predicate takes in a command's context, which includes the guild where the command was coming from.
    # We use this to make sure people can't use Professor flitwick from other servers and have it affect the Dueling server.
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id

    return commands.check(predicate)
