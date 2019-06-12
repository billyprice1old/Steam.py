import discord
from discord.ext import commands
import aiohttp
from .utils import Utils
import requests

class Steammain:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, vanityurl):
        """Get information on a user (requires VanityURl)"""

        message = await self.bot.say("Getting Information...")
        # Convert VanityURL to SteamID64
        steamid = await Utils.vanitytosteamid(vanityurl)
        # Get player Info
        userinfo = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=FF0EEF99E5BD63F29FC0F938A56F115C&steamids=" + steamid)
        userjson = userinfo.json()
        userjson = userjson['response']['players'][0]

        try:
            realname = userjson['realname']
        except KeyError:
            realname = "None Set"
        # Print Embed
        embed = discord.Embed(title="Steam User Information", url=userjson['profileurl'],
                              description="Information on Requested User (SteamID) " + userjson['steamid'], color=0x1ea632)
        embed.set_thumbnail(url=userjson['avatarfull'])
        embed.add_field(name="Username:", value = userjson['personaname'], inline=True)
        embed.add_field(name="Real Name:", value = realname, inline = True)
        embed.add_field(name="Primary Group ID:", value = userjson['primaryclanid'], inline = False)
        await self.bot.edit_message(message, new_content="User Information Found!", embed=embed)

    @commands.command()
    async def vacban(self, user):
        """Check if a user is VAC Banned or community banned (use SteamID 64 or VanityURL)"""
        # check if its a steamid or url
        message = await self.bot.say("Checking...")
        if not user.isdigit():
            steamid = requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FF0EEF99E5BD63F29FC0F938A56F115C&vanityurl=" + user)
            steamid = steamid.json()
            if steamid['response']['success'] != 1:
                await self.bot.say(
                    "There was an error contacting the Steam API (Converting URL to SteamID64). Error Message: " +
                    steamid['response']['message'])
                return
            user = steamid['response']['steamid']

        data = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=FF0EEF99E5BD63F29FC0F938A56F115C&steamids=" + user)
        datajson = data.json()
        datajson = datajson['players'][0]
        embed = discord.Embed(title="Steam User Ban Information", description="User ban info for SteamID " + user,
                              color=0xc21010)
        embed.set_thumbnail(url="https://i.imgur.com/tq43DIX.png")
        embed.add_field(name="VAC Banned", value=datajson['VACBanned'], inline=True)
        embed.add_field(name="VAC Ban Count", value=datajson['NumberOfVACBans'], inline=True)
        embed.add_field(name="Community Banned", value=datajson['CommunityBanned'], inline=True)
        embed.add_field(name="Game Ban Count", value=datajson['NumberOfGameBans'], inline=True)
        embed.set_footer(
            text="Information Incorrect? Check first that you spelled the name correctly, then report this to the bot author.")
        await self.bot.edit_message(message, new_content="Information Found!", embed=embed)



def setup(bot):
    bot.add_cog(Steammain(bot))
