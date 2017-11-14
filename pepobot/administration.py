print("IMPORT: %s" % __name__)

from . import config
from . import discord
from . import functions
from . import entropy

@discord.bot.command(pass_context=True, no_pm=True, hidden=True, aliases=config.cfg['bot']['commands']['fetchimage'])
async def fetchimage(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        resp = await functions.fetchFrogFromMessage(ctx.message)
        if resp is False:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        else:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['success'])

@discord.bot.command(pass_context=True, no_pm=True, hidden=True, aliases=config.cfg['bot']['commands']['recallimage'])
async def recallimage(ctx, id: str):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        recalled = await discord.bot.get_message(ctx.message.channel, id)
        getFroggo = await functions.fetchFrogFromMessage(recalled)
        if getFroggo is False:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        else:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['success'])

@discord.bot.group(pass_context=True, no_pm=True, hidden=True, aliases=config.cfg['bot']['commands']['admin'])
async def imagebotadmin(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        if ctx.invoked_subcommand is None:
            await discord.bot.say('Unknown request')

@imagebotadmin.command(pass_context=True, no_pm=True, hidden=True)
async def resetpool(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        health = entropy.findPoolHealth() * 100
        if entropy.resetPool() is True:
            await discord.bot.say('Reset the image entropy pool, {0} in randomized pool. Pool was {1}% before reset.'.format(len(entropy.frogPool), health))

@imagebotadmin.command(pass_context=True, no_pm=True, hidden=True)
async def reloadconfig(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        cf = config.loadConfig()
        if cf is True:
            await discord.bot.say('config.json successfully and carefully reloaded in place.')
        else:
            await discord.bot.say('Unable to reload config.json in place. Parser returned: {0}'.format(cf))