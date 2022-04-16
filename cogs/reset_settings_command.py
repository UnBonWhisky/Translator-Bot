import discord
from discord import Intents
from discord.ext import commands,tasks
from discord.ext.commands import Bot, CommandNotFound, ChannelNotFound
from discord.utils import get

from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_components
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

from datetime import timezone, tzinfo, timedelta
import sqlite3
import random
import asyncio
import os
import googletrans
from googletrans import Translator

db = sqlite3.connect("translator.sqlite") # Ouverture de la base de données
cursor = db.cursor()

trad = Translator(service_urls=['translate.googleapis.com'])

class ResetSettingsSlash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name = "resetsettings", description = "Command for servers admins. Erase all datas including channel languages and default language")
    async def resetsettings(self, ctx : SlashContext):

        if ctx.author.guild_permissions.administrator:

            EmbedAreYouSure = discord.Embed(description = "Are you sure you want to erase all datas of your server on the bot ?\nYou got 2 minutes to react",
                                            colour = discord.Colour.dark_red())
            
            EmbedCancelled = discord.Embed(description = "You didn't react in the 2 minutes given or you clicked on the ❌ reaction.\nReset task cancelled.",
                                        colour = discord.Colour.purple())
            
            MessageSure = await ctx.send(embed = EmbedAreYouSure)

            await MessageSure.add_reaction('✅')
            await MessageSure.add_reaction('❌')

            def CheckSure(reaction, user):
                return user.id == ctx.author.id and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌') and reaction.message.id == MessageSure.id 
            
            try:

                reaction, user = await self.client.wait_for('reaction_add', timeout=120.0, check = CheckSure)

            except asyncio.TimeoutError:
                try:
                    await MessageSure.clear_reactions()
                except discord.Forbidden:
                    pass
                await MessageSure.edit(embed = EmbedCancelled)
                await asyncio.sleep(10)
                await MessageSure.delete()
                return

            else:
                if str(reaction.emoji) == '✅' :

                    cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
                    DefaultLG = cursor.fetchone()

                    if str(DefaultLG) == "None" or str(DefaultLG) == "(None,)":

                        pass

                    else :

                        cursor.execute(f"DELETE FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
                        db.commit()
                    
                    cursor.execute(f"SELECT * FROM guild{ctx.guild.id}")
                    ischannelinlist = cursor.fetchall()

                    if str(ischannelinlist) == "None" or str(ischannelinlist) == "(None,)" :

                        pass

                    else :

                        cursor.execute(f"DELETE FROM guild{ctx.guild.id}")
                        db.commit()

                    EmbedFinished = discord.Embed(description = "All datas of your server has been erased !",
                                                colour = discord.Colour.green())
                    
                    
                    await MessageSure.clear_reactions()
                    await MessageSure.edit(embed = EmbedFinished)

                    
                elif str(reaction.emoji) == '❌' :
                    try:
                        await MessageSure.clear_reactions()
                    except discord.Forbidden:
                        pass
                    await MessageSure.edit(embed = EmbedCancelled)
                    await asyncio.sleep(10)
                    try:
                        await MessageSure.delete()
                    except Exception:
                        pass


def setup(client):
    client.add_cog(ResetSettingsSlash(client))
    print("Reset Settings Command cog ready !")
