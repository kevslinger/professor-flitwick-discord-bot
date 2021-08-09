import datetime
import time
import constants
import discord_ids
import discord
from discord.ext.tasks import loop
from discord.ext import commands
from asyncprawcore.exceptions import AsyncPrawcoreException
from modules.reddit_feed.reddit_post import RedditPost
from utils import reddit_utils, logging_utils, discord_utils

# Reddit feed settings
CHECK_INTERVAL = 5  # seconds to wait before checking again
SUBMISSION_LIMIT = 5  # number of submissions to check


class RedditFeedCog(commands.Cog, name="Reddit Feed"):
    """Listens to r/Dueling and sends posts to #Announcements"""

    def __init__(self, bot):
        self.bot = bot
        self.reddit = reddit_utils.create_reddit_client()

    @commands.Cog.listener()
    async def on_ready(self):
        """When discord is connected"""
        # Start Reddit loop
        self.reddit_feed.start()

    @commands.command(name="resend")
    @commands.has_permissions(administrator=True)
    @discord_utils.is_in_guild(discord_ids.DUELING_DISCORD_ID)
    async def resend(self, ctx):
        """Command to resend the last r/Dueling post again. Only for admins.

		Usage: `!resend`"""
        # log command in console
        await logging_utils.log_command("resend", ctx.channel, ctx.author)
        # respond to command
        await ctx.send("Resending last announcement!")
        # check for last submission in subreddit
        subreddit = await self.reddit.subreddit()
        async for submission in subreddit.new(limit=1):
            # process submission
            subreddit, title, author, message = RedditPost(self.bot, submission).process_post()
            embed = discord.Embed(title=title,
                                  description=f"By u/{author}")
            embed.add_field(name=f"New Post in r/{subreddit}!",
                            value=message,
                            inline=False)
            channel = self.bot.get_channel(discord_ids.ANNOUNCEMENTS_CHANNEL_ID)
            await channel.send(embed=embed)

    @loop(seconds=CHECK_INTERVAL)
    async def reddit_feed(self):
        """loop every few seconds to check for new submissions"""
        try:
            # check for new submission in subreddit
            subreddit = await self.reddit.subreddit(constants.DUELING_SUBREDDIT)
            async for submission in subreddit.new(limit=SUBMISSION_LIMIT):
                # check if the post has been seen before
                if not submission.saved:
                    # save post to mark as seen
                    await submission.save()
                    # process submission
                    subreddit, title, author, message = RedditPost(self.bot, submission).process_post()
                    embed = discord.Embed(title=title,
                                          description=f"By u/{author}")
                    embed.add_field(name=f"New Post in r/{subreddit}!",
                                    value=message,
                                    inline=False)
                    channel = self.bot.get_channel(discord_ids.ANNOUNCEMENTS_CHANNEL_ID)
                    await channel.send(embed=embed)
        except AsyncPrawcoreException as err:
            print(f"EXCEPTION: AsyncPrawcoreException. {err}")
            time.sleep(10)

    @reddit_feed.before_loop
    async def reddit_feed_init(self):
        """print startup info before reddit feed loop begins"""
        print(f"Logged in: {str(datetime.datetime.now())[:-7]}")
        print(f"Timezone: {time.tzname[time.localtime().tm_isdst]}")
        print(f"Subreddit: {constants.DUELING_SUBREDDIT}")
        print(f"Checking {SUBMISSION_LIMIT} posts every {CHECK_INTERVAL} seconds")


def setup(bot):
    bot.add_cog(RedditFeedCog(bot))
