import discord
from discord.ext import commands
from .utils import Utils


class Dota:
    """Dota Things"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dotainv(self, vanityurl):
        """Get Players Inventory for Dota 2"""

        if not vanityurl.isdigit():
            vanityurl = Utils.vanitytosteamid(vanityurl)
            if not vanityurl:
                await self.bot.say(
                    "There was an error contacting the Steam API (Converting URL to SteamID64). "
                    "Confirm you spelled the user correctly, then p"
                    "lease report this to the bot author, DJ Electro#8890")
                return
        message = await self.bot.say("Contacting Steam API.")



def setup(bot):
    bot.add_cog(Dota(bot))
