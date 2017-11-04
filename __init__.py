import pepobot.config
import pepobot.discord
import pepobot.functions
import pepobot.analytics

import pepobot.scraper
import pepobot.poster

#start the discord connection
pepobot.discord.bot.run(pepobot.config.cfg['bot']['token'])