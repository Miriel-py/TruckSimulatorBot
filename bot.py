from os import getenv
import sys
import asyncio
import logging
from datetime import datetime
import discord
from discord.ext import commands
from discord_slash import SlashCommand
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
    bot = commands.Bot(command_prefix=["t.", "T."], help_command=None, case_insensitive=True)

    SlashCommand(bot, sync_commands=True)
    logger = logging.getLogger()

    if "--debug" in sys.argv:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logging.getLogger("discord.gateway").setLevel(logging.WARNING)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(config.LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(console_handler)

    if "--enable-log-file" in sys.argv:
        file_handler = logging.FileHandler("./logs/{}.log".format(datetime.now().strftime("%Y-%m-%d_%H:%M")))
        file_handler.setFormatter(logging.Formatter(config.LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(file_handler)
        logging.info("Logging into file is enabled")

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

    @bot.command(aliases=["truck", "drive", "job"])
    async def help(ctx):
        await ctx.channel.send(
            embed=discord.Embed(
                title="Hey there fellow Trucker",
                description="This bot has switched to slash commands. "
                "Just type / and you will see a list of all available commands. "
                "If you don't see them, make sure you have the permission to use application commands and your server "
                "admin granted the bot the slash commands scope using [this link]"
                "(https://discord.com/api/oauth2/authorize?client_id=831052837353816066&permissions=3072&scope=bot%20applications.commands).",
                colour=discord.Colour.gold(),
            )
        )

    @bot.event
    async def on_ready():
        scheduler.start()

    asyncio.run(players.init())
    bot.run(BOT_TOKEN)
    asyncio.run(players.close())


if __name__ == "__main__":
    main()
