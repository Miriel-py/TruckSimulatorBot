from os import getenv
import sys
import asyncio
import logging
from datetime import datetime
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv
import api.players as players

import config

from system import System
from driving import Driving
from stats import Stats
from economy import Economy
from gambling import Gambling
from misc import Misc
from truck import Trucks

load_dotenv("./.env")
BOT_TOKEN = getenv("BOT_TOKEN", default="")
INGAME_NEWS_CHANNEL_ID = int(getenv("INGAME_NEWS_CHANNEL_ID", default=0))


def main():
    intents = discord.Intents.none()
    intents.guilds = True
    bot = commands.Bot(command_prefix="", help_command=None, case_insensitive=True, intents=intents)

    logger = logging.getLogger()

    if "--debug" in sys.argv:
        SlashCommand(bot, sync_commands=True, debug_guild=830928381100556338)
        logger.setLevel(logging.DEBUG)
    else:
        SlashCommand(bot, sync_commands=True)
        logger.setLevel(logging.INFO)
        logging.getLogger("discord.gateway").setLevel(logging.WARNING)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(config.LOG_FORMAT))
    logger.addHandler(console_handler)

    scheduler = AsyncIOScheduler()

    driving_commands = Driving(bot)
    economy_commands = Economy(bot, scheduler, INGAME_NEWS_CHANNEL_ID, driving_commands)
    bot.add_cog(System(bot, driving_commands))
    bot.add_cog(driving_commands)
    bot.add_cog(Stats(bot))
    bot.add_cog(economy_commands)
    bot.add_cog(Gambling(bot))
    bot.add_cog(Misc())
    bot.add_cog(Trucks(bot, driving_commands))

    @bot.event
    async def on_ready():
        scheduler.start()

    asyncio.run(players.init())
    bot.run(BOT_TOKEN)
    asyncio.run(players.close())


if __name__ == "__main__":
    main()
