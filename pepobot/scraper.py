print("IMPORT: %s" % __name__)

from . import config
from . import discord 
from . import functions

@discord.bot.event
async def on_reaction_add(reaction, user):
    #trigger the add sequence by reaction of an image on any server by the bot owner
    if user.id == config.cfg['administration']['owner'] and reaction.emoji == "✅":
        getFroggo = await functions.fetchFrogFromMessage(reaction.message)
        if getFroggo is False:
            await discord.bot.add_reaction(reaction.message, config.cfg['reaction']['failure'])
        else:
            await discord.bot.add_reaction(reaction.message, config.cfg['reaction']['success'])