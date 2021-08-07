import discord
import discord_ids
from typing import Union


async def log_command(command: str, channel: discord.TextChannel, author: Union[discord.User, discord.Member]) -> None:
    """Log the command used, what channel it's in, and who used it"""
    # If command was used in a server's channel (not in DMs)
    if hasattr(channel, "name"):
        print(f"Received {command} from {author} in {channel.name}")
        # In the dueling server we have a bot-logs channel where we log each command usage.
        if channel.guild.id == discord_ids.DUELING_DISCORD_ID:
            embed = discord.Embed(author=author,
                                  description=f"Used `{command}` in {channel.mention}")
            embed.set_author(name=f"{author}", icon_url=author.avatar_url)
            log_channel = channel.guild.get_channel(discord_ids.BOT_LOG_CHANNEL_ID)
            await log_channel.send(embed=embed)
    else:
        print(f"Received {command} from {author} in DM")
