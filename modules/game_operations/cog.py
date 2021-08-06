from discord.ext import commands


class GameOpsCog(commands.Cog, name="Game Operations"):
    """Commands for Game Hosts to start and end dueling games"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="openlobby")
    async def openlobby(self, ctx):
        """Unlocks lobby, posts a welcome message like how to use !join, tag @TriviaTuesday"""
        pass

    @commands.command(name="startgame", aliases=["start"])
    async def startgame(self, ctx):
        """Sends a message on how to sign up for future game pings (i.e. @TriviaTuesday role)
        Locks the lobby,
        Posts a message in #gameplay with instructions
        Tag @CurrentPlayer to say the game is starting"""
        pass
    @commands.command(name="endgame", alises=["end"])
    async def endgame(self, ctx):
        "Removes the CurrentPlayer role from everyone, announces the game has ended"
        pass


def setup(bot):
    bot.add_cog(GameOpsCog(bot))