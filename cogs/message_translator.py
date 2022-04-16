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
import re

db = sqlite3.connect("translator.sqlite") # Ouverture de la base de données
cursor = db.cursor()

trad = Translator(service_urls=['translate.googleapis.com'])

class MessageEventSlash(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        commandornot = await self.client.get_context(message)

        if commandornot.command is not None :
            return
        
        if message.author.bot is True :
            return

        if message.guild is None :
            return

        LANGUAGES = ['none','afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']

        LANGUAGESEXT = ['none','af','sq','am','ar','hy','az','eu','be','bn','bs','bg','ca','ceb','ny','zh-cn','zh-tw','co','hr','cs','da','nl','en','eo','et','tl','fi','fr','fy','gl','ka','de','el','gu','ht','ha','haw','iw','he','hi','hmn','hu','is','ig','id','ga','it','ja','jw','kn','kk','km','ko','ku','ky','lo','la','lv','lt','lb','mk','mg','ms','ml','mt','mi','mr','mn','my','ne','no','or','ps','fa','pl','pt','pa','ro','ru','sm','gd','sr','st','sn','sd','si','sk','sl','so','es','su','sw','sv','tg','ta','te','th','tr','uk','ur','ug','uz','vi','cy','xh','yi','yo','zu']


        cursor.execute(f"SELECT channel_language FROM guild{message.guild.id} WHERE channel_id = {message.channel.id}")
        channeldefaultlanguage = cursor.fetchone()


        if channeldefaultlanguage is not None :

            langue = LANGUAGES.index(channeldefaultlanguage[0])

            source = LANGUAGESEXT[langue]

            if source == "none":
                return
            else:
                MessageEmojis = message.content
                if "\n" in MessageEmojis:
                    MessageEmojis = re.findall(r'\S+|\n',MessageEmojis)

                else:
                    MessageEmojis = " ".join(MessageEmojis.split())
                    MessageEmojis = MessageEmojis.split()
                Mots_A_Supprimer = []

                for No_Spaces in range(len(MessageEmojis)):
                    if MessageEmojis[No_Spaces] == '':
                        Mots_A_Supprimer.append(No_Spaces)
                
                for x in range(len(Mots_A_Supprimer)):
                    del(MessageEmojis[Mots_A_Supprimer[x]])


                Mots_A_Supprimer = []

                for word in range(len(MessageEmojis)):
                    if (str(MessageEmojis[word][0]) == '<') and (str(MessageEmojis[word][-1]) == '>') :
                        Mots_A_Supprimer.append(word)
                
                for x in range(len(Mots_A_Supprimer))[::-1]:
                    del(MessageEmojis[Mots_A_Supprimer[x]])
                
                try:
                    MessageEmojis = ' '.join(MessageEmojis)
                except Exception:
                    pass

                if MessageEmojis is not None :
                    Traduction = trad.translate(text = MessageEmojis, dest=source)

                if Traduction.src == source :
                    return
                
                else :
                    try:
                        await message.reply(Traduction.text)
                    except discord.errors.HTTPException:
                        return
            
        else :

            cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {message.guild.id}")
            DefaultLG = cursor.fetchone()

            if DefaultLG is not None :

                langue = LANGUAGES.index(DefaultLG[0])

                source = LANGUAGESEXT[langue]

                MessageEmojis = message.content
                if "\n" in MessageEmojis:
                    MessageEmojis = re.findall(r'\S+|\n',MessageEmojis)

                else:
                    MessageEmojis = " ".join(MessageEmojis.split())
                    MessageEmojis = MessageEmojis.split()
                Mots_A_Supprimer = []

                for No_Spaces in range(len(MessageEmojis)):
                    if MessageEmojis[No_Spaces] == '':
                        Mots_A_Supprimer.append(No_Spaces)
                
                for x in range(len(Mots_A_Supprimer)):
                    del(MessageEmojis[Mots_A_Supprimer[x]])


                Mots_A_Supprimer = []

                for word in range(len(MessageEmojis)):
                    if (str(MessageEmojis[word][0]) == '<') and (str(MessageEmojis[word][-1]) == '>') :
                        Mots_A_Supprimer.append(word)
                
                for x in range(len(Mots_A_Supprimer))[::-1]:
                    del(MessageEmojis[Mots_A_Supprimer[x]])
                
                try:
                    MessageEmojis = ' '.join(MessageEmojis)
                except Exception:
                    pass

                if MessageEmojis is not None :
                    Traduction = trad.translate(text = MessageEmojis, dest=source)

                if Traduction.src == source :
                    return
                
                else :
                    try:
                        await message.reply(Traduction.text)
                    except discord.errors.HTTPException:
                        return


def setup(client):
    client.add_cog(MessageEventSlash(client))
    print("Message Event cog ready !")
