import logging

from . import config
from . import discord 
from . import functions

from .importers import imgur as imgurimport

logger = logging.getLogger(__name__)
logger.info("loading...")

@discord.bot.event
async def on_reaction_add(reaction, user):
    #trigger the add sequence by reaction of an image on any server by the bot owner
    if user.id == config.cfg['administration']['owner'] and reaction.emoji == "✅":
        getFroggo = await functions.fetchFrogFromMessage(reaction.message)
        if getFroggo is False:
            await discord.bot.add_reaction(reaction.message, config.cfg['reaction']['failure'])
        else:
            await discord.bot.add_reaction(reaction.message, config.cfg['reaction']['success'])

@discord.bot.group(pass_context=True, no_pm=True, hidden=True)
async def massimporter(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        if ctx.invoked_subcommand is None:
            await discord.bot.say('Method is either not supported or an error happened :(. Supports imgur...')

@massimporter.command(pass_context=True, no_pm=True, hidden=True)
async def imgur(ctx, url: str):
    if ctx.message.author.id == config.cfg['administration']['owner']:
    	await discord.bot.say('Working on that... This does not run async and might break the bot on long imports.')
    	out = imgurimport.imgur(url)