from discord.ext import commands
from .utils import Utils
import aiohttp
import asyncio


class Userinfo:
    """User Related Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ownedgames(self, ctx, *, user):
        """Get games owned by a user (use SteamID64 or VanityURL)"""

        session = aiohttp.ClientSession()
        orimessage = await self.bot.say("Contacting API... (This will DM The list to you, and may take a very, VERY, "
                                        "long time.")
        if not user.isdigit():
            user = await Utils.vanitytosteamid(user)
        async with session.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=FF0EEF99E5BD63F29FC0F938A56F115C&steamid=" + user) as r:
            ownedgames = await r.json()
        ownedgames = ownedgames['response']['games']
        message = "```"
        for i in ownedgames:
            game = await Utils.idtogame(i['appid'])
            playtime = i['playtime_forever']
            message = message + "\n" + str(game) + " -- " + str(playtime) + " minutes"
        message = message + "```"
        await self.bot.edit_message(orimessage, new_content="DMing list to you now.")
        await self.bot.whisper(message)
        session.close()


def setup(bot):
    bot.add_cog(Userinfo(bot))
