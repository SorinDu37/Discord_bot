"""
This file will load all information and set-up loaders for the program.
Sorin I. Gherasim
25/06/2026
"""

import discord
from dotenv import load_dotenv
import os
import sqlite3
import logging
from discord.ext import commands
from src.query_registry import QueryRegistry
from src.cogs import VocalRewardEvents, Progression, Admin

BOT_PREFIX = '!' #modify to change bot prefix
DB_NAME = 'bot_database.db'

SQL_SCHEMA_PATH = './database/schema.sql'
SQL_QUERIES_PATH = './database/queries.sql'

def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #read and exec SQL init file
    try:
        with open(SQL_SCHEMA_PATH, 'r') as f :
            sql_script = f.read()
        cursor.executescript(sql_script)
        conn.commit()
    except FileNotFoundError:
        logging.getLogger('discord').error("Initialization failed: 'schema.sql' file not found.")
    finally:
        conn.close()

async def start_up() :
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    initialize_database()

    queries = QueryRegistry(SQL_QUERIES_PATH)

    db_conn = sqlite3.connect(DB_NAME)

    handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
    intents = discord.Intents.all()
    

    bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

    await bot.add_cog(VocalRewardEvents(bot, db_conn, queries))
    await bot.add_cog(Progression(bot, db_conn, queries))
    await bot.add_cog(Admin(bot,db_conn, queries))

    discord.utils.setup_logging(handler=handler, level=logging.DEBUG)

    await bot.start(token)