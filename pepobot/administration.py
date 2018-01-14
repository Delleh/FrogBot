import logging

from . import config
from . import discord
from . import functions
from . import entropy

import subprocess
import sys

logger = logging.getLogger(__name__)
logger.info("loading...")

@discord.bot.command(pass_context=True, hidden=True, aliases=config.cfg['bot']['commands']['fetchimage'])
async def fetchimage(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        resp = await functions.fetchFrogFromMessage(ctx.message)
        if resp is False:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        else:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['success'])

@discord.bot.command(pass_context=True, hidden=True, aliases=config.cfg['bot']['commands']['recallimage'])
async def recallimage(ctx, id: str):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        recalled = await discord.bot.get_message(ctx.message.channel, id)
        getFroggo = await functions.fetchFrogFromMessage(recalled)
        if getFroggo is False:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        else:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['success'])

@discord.bot.group(pass_context=True, hidden=True, aliases=config.cfg['bot']['commands']['admin'])
async def imagebotadmin(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        if ctx.invoked_subcommand is None:
            await discord.bot.say('Unknown request. Did you mean resetpool | reloadconifg | stats | git | host?')

@imagebotadmin.command(pass_context=True, hidden=True)
async def resetpool(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        health = entropy.findPoolHealth() * 100
        if entropy.resetPool() is True:
            await discord.bot.say('Reset the image entropy pool, {0} in randomized pool. Pool was {1}% before reset.'.format(len(entropy.frogPool), health))

@imagebotadmin.command(pass_context=True, hidden=True)
async def reloadconfig(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        cf = config.loadConfig()
        if cf is True:
            await discord.bot.say('config.json successfully and carefully reloaded in place.')
        else:
            await discord.bot.say('Unable to reload config.json in place. Parser returned: {0}'.format(cf))

@imagebotadmin.command(pass_context=True, hidden=True)
async def stats(ctx):
    usercount = 0
    for ayylmao in discord.bot.get_all_members(): usercount = usercount + 1
    await discord.bot.say('Currently in {0} Discords shitposting to {1} users'.format(len(discord.bot.servers), usercount))

@imagebotadmin.command(pass_context=True, hidden=True)
async def git(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        gitcommit = subprocess.check_output(['git','rev-parse','--short','HEAD']).decode(encoding='UTF-8').rstrip()
        gitbranch = subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD']).decode(encoding='UTF-8').rstrip()
        gitremote = subprocess.check_output(['git','config','--get','remote.origin.url']).decode(encoding='UTF-8').rstrip().replace(".git","")
        await discord.bot.say("```Commit {0}, Branch {1}, Remote {2}```".format(gitcommit, gitbranch, gitremote))

@imagebotadmin.command(pass_context=True, hidden=True)
async def host(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        await discord.bot.say("```Discord.py {0}, Python {1} ({2})```".format(discord.discord.__version__, sys.version, sys.platform))


#probably come up with a better place for this
@discord.bot.event
async def on_server_join(server):
    msg = "**Joined server:** `{0.name}` **Owner:** `{0.owner.name}#{0.owner.discriminator}` **Members:** `{0.member_count}`".format(server)
    logger.info(msg)
    await discord.bot.send_message(discord.objectFactory(config.cfg['administration']['requests']),msg)
@discord.bot.event
async def on_server_remove(server):
    msg = "**Departing server:** `{0.name}` **Owner:** `{0.owner.name}#{0.owner.discriminator}` **Members:** `{0.member_count}`".format(server)
    logger.info(msg)
    await discord.bot.send_message(discord.objectFactory(config.cfg['administration']['requests']),msg)