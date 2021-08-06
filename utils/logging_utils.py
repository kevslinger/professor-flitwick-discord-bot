import constants

def log_command(command: str, channel, author: str) -> None:
    """Log the command used, what channel it's in, and who used it"""
    print(f"Received {command} from {author} in {channel.name if hasattr(channel, 'name') else 'DM'}")
    if channel.guild.id == constants.DUELING_DISCORD_ID:
        embed = discord.Embed(author=author,
                              description=f"Used `{command}` in {channel.mention}")
    # TODO: Log commands in bot-logs channel in dueling server 872967948409655336