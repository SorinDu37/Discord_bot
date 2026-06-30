import discord
from discord.ext import commands

class Admin(commands.Cog) :
    def __init__(self, bot, db_conn, queries) :
        self.bot = bot
        self.conn = db_conn
        self.cursor = self.conn.cursor()

        self.queries = queries