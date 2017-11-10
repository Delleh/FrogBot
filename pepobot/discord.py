print("IMPORT: %s" % __name__)

import discord
from . import config
from . import entropy
from discord.ext import commands

bot = commands.Bot(command_prefix=config.cfg['bot']['prefix'], description=config.cfg['bot']['description'])

@bot.event
async def on_ready():
    entropy.resetPool()
    print("HELLO: Logged in to Discord as '{0.user.name}' ({0.user.id})".format(bot))

def objectFactory(snowflake):
    return discord.Object(snowflake)