import aiohttp
import asyncio
import async_timeout


class Utils:

    async def vanitytosteamid(vanityurl):
        """Convert a vanity url to SteamID64"""

        session = aiohttp.ClientSession()
        async with session.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FF0EEF99E5BD63F29FC0F938A56F115C&vanityurl=" + vanityurl) as r:
            resjson = await r.json()
        if resjson['response']['success'] != 1:
            session.close()
            return False
        session.close()
        return resjson['response']['steamid']

    async def gametoid(gamename):
        """Convert a game name to its ID"""
        session = aiohttp.ClientSession()

        async with session.get("http://api.steampowered.com/ISteamApps/GetAppList/v2") as r:
            response = await r.json()
        response = response['applist']['apps']
        try:
            gameid = next((item for item in response if item["name"] == gamename))
        except StopIteration:
            session.close()
            return False
        gameid = gameid['appid']
        session.close()
        return gameid

    async def idtogame(gameid):
        """Convert game ID to game name"""

        session = aiohttp.ClientSession()
        async with session.get("http://api.steampowered.com/ISteamApps/GetAppList/v2") as r:
            response = await r.json()
        response = response['applist']['apps']
        try:
            gamename = next((item for item in response if item["appid"] == gameid))
        except StopIteration:
            session.close()
            return False
        gamename = gamename['name']
        session.close()
        return gamename

    def setup(self):
        pass
