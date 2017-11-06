print("IMPORT: %s" % __name__)

from . import config
from . import discord
from . import functions

@discord.bot.command(pass_context=True, description="Posts frogs")
async def pepo(ctx):
    chosenFrog = functions.randomFrog()
    with open(chosenFrog, "rb") as f:
        await discord.bot.send_file(ctx.message.channel, f)

@discord.bot.command(pass_context=True, no_pm=True)
async def fetch(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        resp = await functions.fetchFrogFromMessage(ctx.message)
        if resp is False:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        else:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['success'])

@discord.bot.command(pass_context=True, no_pm=True)
async def recall(ctx, id: str):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        recalled = await discord.bot.get_message(ctx.message.channel, id)
        getFroggo = await functions.fetchFrogFromMessage(recalled)
        if getFroggo is False:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        else:
            await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['success'])

@discord.bot.command(pass_context=True, no_pm=True)
async def peporequest(ctx):
    filename = await functions.queueFrogFromMessage(ctx.message)

    if filename is False:
        await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        return
    
    #check to make sure filetype is valid based on hex data not ext
    filenameCheck = functions.getFileType(filename)
    if filenameCheck is False:
        await discord.bot.add_reaction(ctx.message, config.cfg['reaction']['failure'])
        return

    #if we made it this far put it in the pepo-request channel
    await discord.bot.send_message(discord.objectFactory(config.cfg['administration']['requests']),"New suggestion from: **" + ctx.message.author.name + "** from server: **" + ctx.message.server.name + "**")
    with open(filename, "rb") as f:
        await discord.bot.send_file(discord.objectFactory(config.cfg['administration']['requests']), f)
    functions.deleteFrog(filename)