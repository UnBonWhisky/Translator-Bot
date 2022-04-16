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

class DefaultLanguageSlash(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    ###############
    # set command #
    ###############

    @cog_ext.cog_subcommand(base="defaultlanguage", name="set", description="Command for servers admins. Used to set a default language for the server (1 for the full server)", options=[
        create_option(name="language", description="Language you want to set. Refer to languagelist to see available languages. ", option_type=3, required=True)
    ])
    async def defaultlanguage_set(self, ctx : SlashContext, language):

        if ctx.author.guild_permissions.administrator:

            LANGUAGES = ['afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']
            

            cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
            DefaultLG = cursor.fetchone()

            if language in LANGUAGES :

                if str(DefaultLG) == "None" :

                    sql = ("INSERT INTO default_guild_language(guild_id, default_language) VALUES(?,?)")
                    val = (ctx.guild.id, language)
                    cursor.execute(sql, val)
                    db.commit()

                    EmbedLanguage = discord.Embed(description = "Default Language set !",
                                                colour = discord.Colour.green())
                
                else :

                    sql = ("UPDATE default_guild_language SET default_language = ? WHERE guild_id = ?")
                    val = (language, ctx.guild.id)
                    cursor.execute(sql, val)
                    db.commit()

                    EmbedLanguage = discord.Embed(description = "Default Language updated !",
                                                colour = discord.Colour.green())
            
            else :

                EmbedLanguage = discord.Embed(description = "I can't translate to this language.\nType ``%languagelist`` to have the full language list",
                                            colour = discord.Colour.red())
            
            await ctx.send(embed = EmbedLanguage, hidden=True)

        else :

            await ctx.send(content= "You are not allowed to use this command.\nOnly admins can use this command.", hidden=True)
    

    #################
    # reset command #
    #################

    @cog_ext.cog_subcommand(base="defaultlanguage", name="reset", description="Command for servers admins. Used to remove the default language of the server")
    async def defaultlanguage_reset(self, ctx: SlashContext):

        if ctx.author.guild_permissions.administrator:

            cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
            DefaultLG = cursor.fetchone()

            if str(DefaultLG) == "None" or str(DefaultLG) == "(None,)":

                EmbedDeleted = discord.Embed(description = "You didn't put any default language before",
                                            colour = discord.Colour.red())
            
            else:

                cursor.execute(f"DELETE FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
                db.commit()

                EmbedDeleted = discord.Embed(description = "Default Language has been deleted !",
                                            colour = discord.Colour.green())

            await ctx.send(embed = EmbedDeleted, hidden=True)
        
        else :

            await ctx.send(content= "You are not allowed to use this command.\nOnly admins can use this command.", hidden=True)
    

    ###############
    # see command #
    ###############

    @cog_ext.cog_subcommand(base="defaultlanguage", name="see", description="Command for servers admins. Used to see the default language of the server")
    async def defaultlanguage_see(self, ctx: SlashContext):

        if ctx.author.guild_permissions.administrator:
        
            cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
            DefaultLG = cursor.fetchone()
            
            if str(DefaultLG) == "None" or str(DefaultLG) == "(None,)":

                EmbedNone = discord.Embed(title="You didn't have a default language before this command.",
                                        description= "You can use ``/defaultlanguage set <language in the languagelist command>`` to set a default language for the server.",
                                        colour = discord.Colour.red())

            else:

                EmbedNone = discord.Embed(title = "Here is your default language :",
                                    description = f"{DefaultLG[0]}",
                                    colour = discord.Colour.purple())

            await ctx.send(embed = EmbedNone, hidden=True)

        else :

            await ctx.send(content= "You are not allowed to use this command.\nOnly admins can use this command.", hidden=True)




def setup(client):
    client.add_cog(DefaultLanguageSlash(client))
    print("Default Language Command cog ready !")
