"""
This file contains all events linked to the bot.
Sorin I. Gherasim
25/06/2026
"""

import discord
from discord.ext import commands,tasks
from datetime import datetime
import logging

LOOP_DELAY = 3.0


logger = logging.getLogger('discord')

class VocalRewardEvents(commands.Cog) :

    def __init__(self,bot) : 
        self.bot = bot
        self.voice_trackers = {} #map user_id ->timestamp

        self.reward_sweeper.start()

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after) :

        if before.channel is None and after.channel is not None : #if it's a join
            date = datetime.now()
            self.voice_trackers[member.id] = date

            logger.info(f"Tracking started : {member.name}, joined {after.channel.name} at {date}")
        
        elif before.channel is not None and after.channel is None : #if it's a leave
            join_time = self.voice_trackers.pop(member.id, None)

            if join_time is None :
                self.errors_logging(
                    'USER_LEFT_WITHOUT_JOIN',
                    member.name,
                    channel_name = before.channel,
                    id = member.id
                    )
            
            end_date = datetime.now()
            duration = (end_date - join_time).total_seconds()

            logger.info(f"Tracking ended : {member.name}, left {before.channel.name} at {end_date}")

    @tasks.loop(minutes= LOOP_DELAY)
    async def reward_sweeper(self):
        for guild in self.bot.guilds:
            active_channels = [vc for vc in guild.voice_channels if len(vc.members) >= 1]
            for voice_channel in active_channels:
                for member in voice_channel.members:
                    if member.bot or member.voice.self_mute  :
                        continue

                    logger.info(f"Awarded {LOOP_DELAY} minutes reward to {member.name} (ID : {member.id})")

            
    def errors_logging(self, type, *args, **kwargs) :
        match type:
            case 'USER_LEFT_WITHOUT_JOIN' :
                user_name = args[0] if args else "Unknown User"
                channel = kwargs.get('channel_name', "Unknown Channel")
                id = kwargs.get('id', "Unknown ID")

                logger.info(f"NON-FATAL ERROR DETECTECTED : User {user_name} (ID : {id}) has left channel {channel} without prior occurence \
                             of him joining it. Could be due to restart of the bot.")

    @reward_sweeper.before_loop
    async def before_sweeper(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(VocalRewardEvents(bot))
