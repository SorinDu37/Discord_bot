import discord
from discord.ext import commands
from src.base_cog import DatabaseMixIn

class Admin(DatabaseMixIn, commands.Cog) :
    def __init__(self, bot, db_conn, queries) :
        DatabaseMixIn.__init__(self,bot,db_conn, queries)
        commands.Cog.__init__(self)