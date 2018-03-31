import logging

from . import config
from . import discord
from . import functions
from . import entropy

import subprocess
import sys
import os
import platform

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
            await discord.bot.say('Unknown request. Did you mean run | resetpool | reloadconifg | stats | system | modules')

@imagebotadmin.command(pass_context=True, hidden=True)
async def run(ctx, *, msg: str):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        try:
            evalData = eval(msg.replace('`',''))
            embedcolor = 0x32CD32
        except Exception as e:
            evalData = e
            embedcolor = 0xDC143C
        emd = discord.embeds.Embed(color=embedcolor)            
        emd.add_field(name="Result", value=evalData)
        await discord.bot.say(embed=emd)

@imagebotadmin.command(pass_context=True, hidden=True)
async def resetpool(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        health = entropy.findPoolHealth() * 100
        if entropy.resetPool() is True:
            await discord.bot.say('Reset the image entropy pool, {0} in randomized pool. Pool was {1:.2f}% before reset.'.format(len(entropy.frogPool), health))

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
    userlist = []
    for member in discord.bot.get_all_members(): userlist.append(member.id)
    await discord.bot.say('Currently in {0:,} Discords shitposting to {1:,} unique users'.format(len(discord.bot.servers), len(set(userlist))))

@imagebotadmin.command(pass_context=True, hidden=True)
async def system(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        load = os.times()
        gitcommit = subprocess.check_output(['git','rev-parse','--short','HEAD']).decode(encoding='UTF-8').rstrip()
        gitbranch = subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD']).decode(encoding='UTF-8').rstrip()
        gitremote = subprocess.check_output(['git','config','--get','remote.origin.url']).decode(encoding='UTF-8').rstrip().replace(".git","")

        emd = discord.embeds.Embed(color=0xE79015)
        emd.add_field(name="Discord.py Version", value=discord.discord.__version__)
        emd.add_field(name="Python Version", value=platform.python_build()[0])
        emd.add_field(name="Host", value="{} ({}) [{}] hostname '{}'".format(platform.system(), platform.platform(), sys.platform, platform.node()))
        emd.add_field(name="Process", value="PID: {} User: {:.2f}% System: {:.2f}%".format(os.getpid(), load[0], load[1]))
        emd.add_field(name="Git Revision", value="`{}@{}` Remote: {}".format(gitcommit.upper(), gitbranch.title(), gitremote))
        await discord.bot.say(embed=emd)

#print what modules have been loaded for the bot
@imagebotadmin.command(pass_context=True, hidden=True)
async def modules(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        mods = ""
        for k in sys.modules.keys():
            if "pepobot" in k:
                mods = mods + "\n" + k
        emd = discord.embeds.Embed(color=0xE79015)
        emd.add_field(name="Loaded Modules", value=mods)
        await discord.bot.say(embed=emd)

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