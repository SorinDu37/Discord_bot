import discord
from discord.ext import commands
from src.base_cog import DatabaseMixIn

class Progression(DatabaseMixIn, commands.Cog) :
    def __init__(self,bot, connection, queries) :
        DatabaseMixIn.__init__(self, bot, connection, queries)
        commands.Cog.__init__(self)
        
        self.cursor.execute("SELECT role_id, required_exp FROM ranks ORDER BY required_exp DESC")
        self.ranks = self.cursor.fetchall()

    async def update_user_rank(self, member : discord.Member) :
        guild = member.guild
        roles = member.roles

        self.cursor.execute("SELECT exp FROM users WHERE user_id = ?", [member.id])
        current_exp = self.cursor.fetchone()[0]

        #add the roles
        eligible_roles = [role_id for role_id, req_exp in self.ranks if current_exp >= req_exp]
        server_eligible_roles = [guild.get_roles(rid) for rid in eligible_roles if guild.get_role(rid)]
        roles_to_add = [role for role in server_eligible_roles if role not in roles]
        if roles_to_add :
            await member.add_roles(*roles_to_add, reason = "EXP rank sync")

        #remove the roles
        not_eligible_roles = [role_id for role_id in self.ranks if role_id not in eligible_roles]
        server_not_eligible_roles = [guild.get_roles(rid) for rid in not_eligible_roles if guild.get_role(rid)]
        roles_to_remove = [role for role in server_not_eligible_roles if role in roles]

        if roles_to_remove :
            await member.remove_roles(*roles_to_remove, reason = "EXP desync corrected")
