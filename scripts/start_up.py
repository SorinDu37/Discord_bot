"""
This file will load all information and set-up loaders for the program.
Sorin I. Gherasim
25/06/2026
"""

import discord
from dotenv import load_dotenv
import os
import logging
from discord.ext import commands

BOT_PREFIX = '!' #modify to change bot prefix

def start_up() :
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

    async def setup_hook() :
        await bot.load_extension('scripts.events') #goes to check setup in events

    bot.setup_hook = setup_hook

    bot.run(token, log_handler=handler, log_level=logging.DEBUG)

    return (handler,bot)