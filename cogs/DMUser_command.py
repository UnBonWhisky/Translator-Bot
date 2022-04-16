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
from requests import options

db = sqlite3.connect("translator.sqlite") # Ouverture de la base de données
cursor = db.cursor()

trad = Translator(service_urls=['translate.googleapis.com'])

class DMMemberSlash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name = "translatechoice", description = "Command for all users. Used to choose where you want your reaction translations.", options=[
        create_option(name = "choice", description = "\"True\" to have translation in DM's. \"False\" to have translation in channel.", option_type=5, required=True)
    ])
    async def translatechoice(self, ctx : SlashContext, choice : bool):

        if choice is True:
            OnOff = "DM"
        else:
            OnOff = "channel"

        if OnOff == "channel" :

            cursor.execute(f"SELECT yesno FROM DMUser WHERE user_id = {ctx.author.id}")
            DMOnOff = cursor.fetchone()

            DMOn = 1

            EmbedActivated = discord.Embed(description = "Reaction Translations will now be sent in the channel !",
                                            colour = discord.Colour.green())
            
            if str(DMOnOff) == "None":

                sql = ("INSERT INTO DMUser(user_id, yesno) VALUES(?,?)")
                val = (ctx.author.id, DMOn)
                cursor.execute(sql, val)
                db.commit()
            
            elif str(DMOnOff) == "(None,)":

                sql = ("UPDATE DMUser SET yesno = ? WHERE user_id = ?")
                val = (DMOn, ctx.author.id)
                cursor.execute(sql, val)
                db.commit()
                    
            await ctx.send(embed = EmbedActivated, hidden=True)
            
        elif OnOff == "DM" :

            cursor.execute(f"SELECT yesno FROM DMUser WHERE user_id = {ctx.author.id}")
            DMOnOff = cursor.fetchone()

            EmbedDeactivated = discord.Embed(description = "Reaction Translations will now be sent in your DMs !",
                                            colour = discord.Colour.green())
            
            if (str(DMOnOff) == "None") or (str(DMOnOff) == "(None,)") :
                pass
            
            else :

                sql = (f"DELETE FROM DMUser WHERE user_id = {ctx.author.id}")
                cursor.execute(sql)
                db.commit()

            await ctx.send(embed = EmbedDeactivated, hidden=True)



def setup(client):
    client.add_cog(DMMemberSlash(client))
    print("DMUser Command cog ready !")
