import discord
from discord.ext import commands
from .utils import Utils
import requests
import time


class GameInfo:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gameinfo(self, *, gamename):
        """Convert game name to ID"""

        message = await self.bot.say("Contacting API")
        appid = await Utils.gametoid(gamename)
        if not appid:
            await self.bot.say("Their was an issue contacting the Steam API. Ensure the game name is spelled correctly"
                               ", then report this to the bot author if the problem continues.")
            return
        embed = discord.Embed(title="Steam Game Information", url="https://store.steampowered.com/app/" + str(appid),
                              description="Info for Requested Game", color=0x42a6cc)
        embed.add_field(name="Steam Game ID", value=appid, inline=True)
        embed.add_field(name="Steam Game Name", value=gamename, inline=True)
        embed.set_footer(text="Hint: use the \"gamenews\" command for the latest news from the game")
        await self.bot.edit_message(message, new_content="Info Found!", embed=embed)

    @commands.command()
    async def gamenews(self, *, game):
        """Get the Latest news for a game"""

        message = await self.bot.say("Contacting API...")
        if not game.isdigit():
            game = await Utils.gametoid(game)
        if not game:
            await self.bot.say("Their was an issue contacting the Steam API. Ensure the game name is spelled correctly"
                               ", then report this to the bot author if the problem continues.")
            return
        news = requests.get("http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?count=1&appid=" + str(game))
        news = news.json()
        news = news['appnews']['newsitems'][0]
        postingtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(news['date']))
        embed = discord.Embed(title="Game Latest News", url=news['url'], description="Latest news post for game.",
                              color=0x1d3a89)
        embed.add_field(name="News Post Title", value=news['title'], inline=True)
        embed.add_field(name="News Post Content", value=news['contents'], inline=True)
        embed.set_footer(text="Posted On: " + postingtime)
        await self.bot.edit_message(message, new_content="Info Found!", embed=embed)


def setup(bot):
    bot.add_cog(GameInfo(bot))
