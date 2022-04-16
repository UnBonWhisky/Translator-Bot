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

class ReactionFlagSlash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name = "allowflag", description = "Command for servers admins. Used to allow or not reactions flag on the server.", options=[
        create_option(name = "allowed", description = "\"True\" to allow flag reactions on your server. \"False\" to don't allow.", option_type=5, required=True)
    ])
    async def allowflag(self, ctx : SlashContext, allowed : bool):

        if ctx.author.guild_permissions.administrator:

            if allowed is True:
                allowed = "enabled"
            elif allowed is False:
                allowed = "disabled"

            cursor.execute(f"SELECT reaction_activated FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
            reaction_allowed = cursor.fetchone()

            if str(reaction_allowed) == "None" :

                sql = ("INSERT INTO default_guild_language(guild_id, reaction_activated) VALUES(?,?)")
                val = (ctx.guild.id, allowed)
                cursor.execute(sql, val)
                db.commit()

                EmbedDone = discord.Embed(description = "Reaction flag setting has been set",
                                        colour = discord.Colour.green()
                                        )
            
            else :

                sql = ("UPDATE default_guild_language SET reaction_activated = ? WHERE guild_id = ?")
                val = (allowed, ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()

                EmbedDone = discord.Embed(description = "Reaction flag setting has been updated",
                                        colour = discord.Colour.green()
                                        )
                
            await ctx.send(embed = EmbedDone, hidden=True)
        
        else :

            await ctx.send(content= "You are not allowed to use this command.\nOnly admins can use this command.", hidden=True)



def setup(client):
    client.add_cog(ReactionFlagSlash(client))
    print("Reaction Language Event Slash cog ready !")
