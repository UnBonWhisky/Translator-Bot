import discord
import asyncio
from discord.ext.commands import Bot, CommandNotFound
from discord.ext import commands, tasks

from discord_slash import cog_ext, SlashContext, ComponentContext

import datetime
from datetime import timezone, tzinfo, timedelta
import time
from discord.utils import get
import logging
import os
import sqlite3
from googletrans import Translator

db = sqlite3.connect("translator.sqlite") # Ouverture de la base de données
cursor = db.cursor()

trad = Translator(service_urls=['translate.googleapis.com'])

class LanguageListSlash(commands.Cog):
    def __init__(self, client):
        self.client = client


    @cog_ext.cog_slash(name = "languagelist", description = "Command for servers admins. Language list supported by the bot")
    async def languagelist(self, ctx : SlashContext):

        if ctx.author.guild_permissions.administrator:

            LANGUAGES = ['afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']

            LanguesDispoA = ""
            LanguesDispoB = ""
            LanguesDispoC = ""
            LanguesDispoD = ""
            LanguesDispoE = ""
            LanguesDispoF = ""
            LanguesDispoG = ""
            LanguesDispoH = ""
            LanguesDispoI = ""
            LanguesDispoJ = ""
            LanguesDispoK = ""
            LanguesDispoL = ""
            LanguesDispoM = ""
            LanguesDispoN = ""
            LanguesDispoO = ""
            LanguesDispoP = ""
            LanguesDispoR = ""
            LanguesDispoS = ""
            LanguesDispoT = ""
            LanguesDispoU = ""
            LanguesDispoV = ""
            LanguesDispoW = ""
            LanguesDispoX = ""
            LanguesDispoY = ""
            LanguesDispoZ = ""
            for x in range (len(LANGUAGES)):
                if LANGUAGES[x][0] == "a":
                    LanguesDispoA += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "b":
                    LanguesDispoB += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "c":
                    LanguesDispoC += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "d":
                    LanguesDispoD += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "e":
                    LanguesDispoE += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "f":
                    LanguesDispoF += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "g":
                    LanguesDispoG += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "h":
                    LanguesDispoH += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "i":
                    LanguesDispoI += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "j":
                    LanguesDispoJ += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "k":
                    LanguesDispoK += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "l":
                    LanguesDispoL += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "m":
                    LanguesDispoM += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "n":
                    LanguesDispoN += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "o":
                    LanguesDispoO += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "p":
                    LanguesDispoP += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "r":
                    LanguesDispoR += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "s":
                    LanguesDispoS += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "t":
                    LanguesDispoT += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "u":
                    LanguesDispoU += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "v":
                    LanguesDispoV += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "w":
                    LanguesDispoW += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "x":
                    LanguesDispoX += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "y":
                    LanguesDispoY += f"{LANGUAGES[x]}\n"
                elif LANGUAGES[x][0] == "z":
                    LanguesDispoZ += f"{LANGUAGES[x]}\n"
                

            EmbedListLanguages = discord.Embed(title = "Available languages to translate",
                                            description = "You can set ``none`` to a channel language to set it as a channel without any translation\n(f.e : channel allowed to speak with multiple languages in it)", 
                                            colour = discord.Colour.purple())

            if LanguesDispoA != "":
                EmbedListLanguages.add_field(name = "A",
                                            value = f"{LanguesDispoA}",
                                            inline = True)
            if LanguesDispoB != "":
                EmbedListLanguages.add_field(name = "B",
                                            value = f"{LanguesDispoB}",
                                            inline = True)
            if LanguesDispoC != "":
                EmbedListLanguages.add_field(name = "C",
                                            value = f"{LanguesDispoC}",
                                            inline = True)
            if LanguesDispoD != "":
                EmbedListLanguages.add_field(name = "D",
                                            value = f"{LanguesDispoD}",
                                            inline = True)
            if LanguesDispoE != "":
                EmbedListLanguages.add_field(name = "E",
                                            value = f"{LanguesDispoE}",
                                            inline = True)
            if LanguesDispoF != "":
                EmbedListLanguages.add_field(name = "F",
                                            value = f"{LanguesDispoF}",
                                            inline = True)
            if LanguesDispoG != "":
                EmbedListLanguages.add_field(name = "G",
                                            value = f"{LanguesDispoG}",
                                            inline = True)
            if LanguesDispoH != "":
                EmbedListLanguages.add_field(name = "H",
                                            value = f"{LanguesDispoH}",
                                            inline = True)
            if LanguesDispoI != "":
                EmbedListLanguages.add_field(name = "I",
                                            value = f"{LanguesDispoI}",
                                            inline = True)
            if LanguesDispoJ != "":
                EmbedListLanguages.add_field(name = "J",
                                            value = f"{LanguesDispoJ}",
                                            inline = True)
            if LanguesDispoK != "":
                EmbedListLanguages.add_field(name = "K",
                                            value = f"{LanguesDispoK}",
                                            inline = True)
            if LanguesDispoL != "":
                EmbedListLanguages.add_field(name = "L",
                                            value = f"{LanguesDispoL}",
                                            inline = True)
            if LanguesDispoM != "":
                EmbedListLanguages.add_field(name = "M",
                                            value = f"{LanguesDispoM}",
                                            inline = True)
            if LanguesDispoN != "":
                EmbedListLanguages.add_field(name = "N",
                                            value = f"{LanguesDispoN}",
                                            inline = True)
            if LanguesDispoO != "":
                EmbedListLanguages.add_field(name = "O",
                                            value = f"{LanguesDispoO}",
                                            inline = True)
            if LanguesDispoP != "":
                EmbedListLanguages.add_field(name = "P",
                                            value = f"{LanguesDispoP}",
                                            inline = True)
            if LanguesDispoR != "":
                EmbedListLanguages.add_field(name = "R",
                                            value = f"{LanguesDispoR}",
                                            inline = True)
            if LanguesDispoS != "":
                EmbedListLanguages.add_field(name = "S",
                                            value = f"{LanguesDispoS}",
                                            inline = True)
            if LanguesDispoT != "":
                EmbedListLanguages.add_field(name = "T",
                                            value = f"{LanguesDispoT}",
                                            inline = True)
            if LanguesDispoU != "":
                EmbedListLanguages.add_field(name = "U",
                                            value = f"{LanguesDispoU}",
                                            inline = True)
            if LanguesDispoV != "":
                EmbedListLanguages.add_field(name = "V",
                                            value = f"{LanguesDispoV}",
                                            inline = True)
            if LanguesDispoW != "":
                EmbedListLanguages.add_field(name = "W",
                                            value = f"{LanguesDispoW}",
                                            inline = True)
            if LanguesDispoX != "":
                EmbedListLanguages.add_field(name = "X",
                                            value = f"{LanguesDispoX}",
                                            inline = True)
            if LanguesDispoY != "":
                EmbedListLanguages.add_field(name = "Y",
                                            value = f"{LanguesDispoY}",
                                            inline = True)
            if LanguesDispoZ != "":
                EmbedListLanguages.add_field(name = "Z",
                                            value = f"{LanguesDispoZ}",
                                            inline = True)


            await ctx.send(embed = EmbedListLanguages, hidden=True)
    
        else :

            await ctx.send(content= "You are not allowed to use this command.\nOnly admins can use this command.", hidden=True)


def setup(client):
    client.add_cog(LanguageListSlash(client))
    print("Language List Command cog ready !")
