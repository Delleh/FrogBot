import pepobot.config
import pepobot.discord
import pepobot.functions
import pepobot.analytics
import pepobot.entropy

import pepobot.scraper
import pepobot.poster
import pepobot.administration

#start the discord connection
pepobot.discord.bot.run(pepobot.config.cfg['bot']['token'])

#TODO: 
# auto make folders in config
# requirements.txt = discordpy, python 3.6.0+
# systemd service template
# peporequest should be generic
# all pepo/frogs should be generic
# custom named !pepo 