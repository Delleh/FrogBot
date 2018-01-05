print("IMPORT: %s" % __name__)

import asyncio
import discord

from . import config
from . import entropy
from discord.ext import commands

bot = commands.Bot(command_prefix=config.cfg['bot']['prefix'], description=config.cfg['bot']['description'])

@bot.event
async def on_ready():
    entropy.resetPool()
    print("HELLO: Logged in to Discord as '{0.user.name}' ({0.user.id})".format(bot))
    print("HELLO: To add this bot to a discord server, use https://discordapp.com/oauth2/authorize?client_id={0.user.id}&scope=bot&permissions=0".format(bot))

    await asyncio.sleep(5)
    print('{0} Setting game status as in as "{1}"'.format(__name__, config.cfg['bot']['playing']))
    await bot.change_presence(game=discord.Game(name=config.cfg['bot']['gamestatus']))    

def objectFactory(snowflake):
    return discord.Object(snowflake)