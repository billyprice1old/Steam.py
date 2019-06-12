from discord.ext import commands
import discord
import logging
import asyncio
import traceback
import sys
from config import Config

description = '''Steam.py Alpha v2.1'''
# Set logging level
logging.basicConfig(level=logging.ERROR)

# this specifies what extensions to load when the bot starts up
startup_extensions = ['cogs.steammain', 'cogs.gameinfo']

# Create the bot object
bot = commands.Bot(command_prefix=Config.botprefix, description=description)


def ownercheck(ctx):
    for i in Config.botowners:
        if i == ctx.message.author.id:
            return True
        else:
            return False


@bot.event
async def on_ready():
    print("© 2017 Electromaster232")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('READY')
    await bot.change_presence(game=discord.Game(name="{} Users and {} Guilds!".format(
        len(set(bot.get_all_members())), len(bot.servers)), type=3))


@commands.check(ownercheck)
@bot.command()
async def load(extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension("cogs.{}".format(extension_name))
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("The extension {} was loaded.".format(extension_name))

@commands.check(ownercheck)
@bot.command()
async def unload(extension_name: str):
    """Unloads an extension."""
    try:
        bot.unload_extension("cogs.{}".format(extension_name))
    except:
        await bot.say("There was an error")
    await bot.say("The extension {} was unloaded.".format(extension_name))

@commands.check(ownercheck)
@bot.command()
async def reload(extension_name: str):
    """Reloads an extension"""
    try:
        bot.unload_extension("cogs.{}".format(extension_name))
    except (AttributeError, ImportError) as error:
        await bot.say("```py\n{}: {}\n```".format(type(error).__name__, str(error)))
        return
    await bot.say("The extension {} was unloaded.".format(extension_name))
    try:
        bot.load_extension("cogs.{}".format(extension_name))
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("The extension {} was loaded.".format(extension_name))


@bot.command()
async def ping():
    """Simple Ping Command"""
    em = discord.Embed(description="Pong!", color=discord.Color.blue())
    await bot.say(embed=em)


@bot.command()
async def owner():
    """Tells you who the bot owner is"""
    owner = str((await bot.application_info()).owner)
    em = discord.Embed(description=owner, color=discord.Color.green())
    await bot.say(embed=em)


@commands.check(ownercheck)
@bot.command(pass_context=True)
async def debug(ctx, *, code):
    """Evaluate Code"""

    global_vars = globals().copy()
    global_vars['bot'] = bot
    global_vars['ctx'] = ctx
    global_vars['message'] = ctx.message
    global_vars['author'] = ctx.message.author
    global_vars['channel'] = ctx.message.channel
    global_vars['server'] = ctx.message.server

    try:
        result = eval(code, global_vars, locals())
        if asyncio.iscoroutine(result):
            result = await result
        result = str(result)
        await bot.say("```" + result + "```")
    except Exception as error:
        await bot.say('```{}: {}```'.format(type(error).__name__, str(error)))
        return


@bot.command()
async def info():
    """Bot Information"""
    await bot.change_presence(game=discord.Game(name="{} Users and {} Guilds!".format(
        len(set(bot.get_all_members())), len(bot.servers)), type=3))
    embed = discord.Embed(title="Bot Info", url="https://gitlab.adamegilbert.me/public/",
                          description="Steam.py bot info", color=0x88ddec)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/133353440385433600/a_5011d8aa9663db347bfc540a955a10f6.gif")
    embed.add_field(name="Bot Author", value="DJ Electro#8890", inline=False)
    embed.add_field(name="Bot Info",
                    value="Steam.py is a multifunction Steam API bot, designed to house complete access to the multiple Steam APIs, allowing you to not have to have multiple Steam bots.",
                    inline=True)
    embed.set_footer(text="Project Started on 3/10/18")
    await bot.say(embed=embed)

@bot.event
async def on_command_error(event, ctx):
    if isinstance(event, commands.CheckFailure):
        await bot.send_message(ctx.message.channel, ":no_entry: Access to this command is restricted.")
    if isinstance(event, commands.MissingRequiredArgument):
        await send_cmd_help(ctx)
    if isinstance(event, commands.CommandNotFound):
        pass
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(event), event, event.__traceback__, file=sys.stderr)


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)


@bot.event
async def on_command(command, ctx):
    embed = discord.Embed(title="Bot command!", description="A command has been ran!", color=0x88ddec)
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.add_field(name="Command Author", value=str(ctx.message.author), inline=True)
    embed.add_field(name="Command Ran", value=str(ctx.message.content), inline=True)
    embed.add_field(name="Server", value=str(ctx.message.server.name), inline=True)
    embed.add_field(name="Author ID", value=str(ctx.message.author.id), inline=True)
    embed.set_footer(text="Steam.py logging system")
    await bot.send_message(bot.get_channel(Config.loggingchannel), embed=embed)

# Load extensions and start the bot
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
# Run the bot object with token
    bot.run(Config.bottoken)
