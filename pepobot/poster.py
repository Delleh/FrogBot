print("Importing... %s" % __name__)

from . import config
from . import discord
from . import functions

@discord.bot.command(pass_context=True, no_pm=True, description="Says Hello :)")
async def hi(ctx):
    await discord.bot.say("<:pepoG:352533294862172160>")

@discord.bot.command(pass_context=True, description="Posts frogs")
async def pepo(ctx):
    chosenFrog = functions.randomFrog()
    with open(chosenFrog, "rb") as f:
        await discord.bot.send_file(ctx.message.channel, f)

@discord.bot.command(pass_context=True, no_pm=True)
async def fetch(ctx):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        URLs = functions.getLinksFromPost(ctx.message.content)
        resp = await functions.getFrogFromURL(ctx.message.id, URLs)
        if resp is False:
            await discord.bot.add_reaction(ctx.message, "ree:287640249964691459")
        else:
            await discord.bot.add_reaction(ctx.message, "pepOk:350323644783656971")

@discord.bot.command(pass_context=True, no_pm=True)
async def recall(ctx, id: str):
    if ctx.message.author.id == config.cfg['administration']['owner']:
        recalled = await discord.bot.get_message(ctx.message.channel, id)
        getFroggo = await functions.fetchFrogFromMessage(recalled)
        if getFroggo is False:
            await discord.bot.add_reaction(ctx.message, "ree:287640249964691459")
        else:
            await discord.bot.add_reaction(ctx.message, "pepOk:350323644783656971")

@discord.bot.command(pass_context=True, no_pm=True)
async def peporequest(ctx):
    filename = await functions.fetchFrogFromMessage(ctx.message)

    if filename is False:
        await discord.bot.add_reaction(ctx.message, "ree:287640249964691459")
        return
    
    #check to make sure filetype is valid based on hex data not ext
    filenameCheck = functions.getFileType(config.cfg['scraper']['location'] + filename)
    if filenameCheck is False:
        await discord.bot.add_reaction(ctx.message, "ree:287640249964691459")
        return

    #if we made it this far put it in the pepo-request channel
    await discord.bot.send_message(discord.objectFactory(config.cfg['administration']['requests']),"New suggestion from: **" + ctx.message.author.name + "** from server: **" + ctx.message.server.name + "**")
    with open(config.cfg['scraper']['staging'] + filename, "rb") as f:
        await discord.bot.send_file(discord.objectFactory(config.cfg['administration']['requests']), f)

    #delete the frog because we really dont want to keep it around and we can just grab on approval
    #TODO: put requests intheir own folder for temp scanning
    functions.deleteFrog(filename)