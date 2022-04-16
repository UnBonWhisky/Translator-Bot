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

class ChannelLanguageSlash(commands.Cog):
    def __init__(self, client):
        self.client = client

    ################
    # list command #
    ################
    
    @cog_ext.cog_subcommand(base="channellanguage", name="list", description="Give the different channel languages you setted up")
    async def channellanguage_list(self, ctx : SlashContext):

        if ctx.author.guild_permissions.administrator:

            cursor.execute(f"SELECT * FROM guild{ctx.guild.id}")
            ChannelLanguageList = cursor.fetchall()

            if str(ChannelLanguageList) == "[]" :

                EmbedMessage = discord.Embed(description = "I didn't found any different language\nType ``/channellanguage add <Channel Mention> <language>`` to have a different language in your channel",
                                        colour = discord.Colour.purple())

            else :

                EmbedMessage = discord.Embed(title = f"{len(ChannelLanguageList)} different(s) language(s) channel(s) found",
                                                    colour = discord.Colour.purple())

                for x in range(len(ChannelLanguageList)):

                    channelname = self.client.get_channel(int(ChannelLanguageList[x][0]))

                    EmbedMessage.add_field(name = f"#{channelname}",
                                            value = f"{ChannelLanguageList[x][1]}",
                                            inline = True)
                
            await ctx.send(embed = EmbedMessage, hidden=True)
        
        else :

            await ctx.send(content="You are not allowed to use this command.\nOnly admins can use this command.", hidden=True)


    ###############
    # add command #
    ###############

    @cog_ext.cog_subcommand(base="channellanguage", name="add", description="Add a different channel languages to your server", options=[
        create_option(name="channel", description="Mention channel of the one you want to set a channel language", option_type=7, required=True),
        create_option(name="language", description="Language you want to set. Refer to languagelist command to see available languages", option_type=3, required=True)
    ])
    async def channellanguage_add(self, ctx : SlashContext, channel, language):
        
        if ctx.author.guild_permissions.administrator:

            LANGUAGES = ['none','afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']

            if language not in LANGUAGES :

                EmbedMessage = discord.Embed(description = "I can't translate this language.\nType ``/languagelist`` to know what languages you can use",
                                        colour = discord.Colour.red())
            
            else :

                cursor.execute(f"SELECT channel_language FROM guild{ctx.guild.id} WHERE channel_id = {channel.id}")
                channelalreadyexist = cursor.fetchone()

                if str(channelalreadyexist) == "None" :

                    sql = (f"INSERT INTO guild{ctx.guild.id}(channel_id, channel_language) VALUES(?,?)")
                    val = (channel.id, language)
                    cursor.execute(sql, val)
                    db.commit()

                    EmbedMessage = discord.Embed(description = "Language has been set !",
                                            colour = discord.Colour.green())
                
                else :

                    sql = (f"UPDATE guild{ctx.guild.id} SET channel_language = ? WHERE channel_id = ?")
                    val = (language, channel.id)
                    cursor.execute(sql, val)
                    db.commit()

                    EmbedMessage = discord.Embed(description = "Language has been updated !",
                                            colour = discord.Colour.green())

            await ctx.send(embed = EmbedMessage, hidden=True)
        
        else :

            await ctx.send(content= "You are not allowed to use this command.\nOnly admins can use this command.", hidden=True)
    
    ##################
    # remove command #
    ##################

    @cog_ext.cog_subcommand(base="channellanguage", name="remove", description="Remove a different channel languages you setted up", options=[
        create_option(name="channel", description="Mention channel of the one you want to remove the channel language", option_type=7, required=True)
    ])
    async def channellanguage_remove(self, ctx : SlashContext, channel):
        
        if ctx.author.guild_permissions.administrator:
                
            cursor.execute(f"SELECT channel_language FROM guild{ctx.guild.id} WHERE channel_id = {channel.id}")
            ischannelinlist = cursor.fetchone()

            if str(ischannelinlist) == "None" or str(ischannelinlist) == "(None,)" :

                EmbedMessage = discord.Embed(description = "This channel has not any different language set !\nPlease give me another channel or type ``/channellanguage list`` to see your different languages setted up.",
                                            colour = discord.Colour.red())
            
            else :

                cursor.execute(f"DELETE FROM guild{ctx.guild.id} WHERE channel_id = {channel.id}")
                db.commit()

                EmbedMessage = discord.Embed(description = "The language of this channel has been deleted !",
                                            colour = discord.Colour.green())
                
            await ctx.send(embed = EmbedMessage, hidden=True)
        
        else :

            await ctx.send(content= "You are not allowed to use this command.\nOnly admins can use this command.", hidden=True)


def setup(client):
    client.add_cog(ChannelLanguageSlash(client))
    print("Channel Language Command cog ready !")
