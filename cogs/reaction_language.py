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

class ReactionEventSlash(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        cursor.execute(f"SELECT reaction_activated FROM default_guild_language WHERE guild_id = {payload.guild_id}")
        reaction_allowed = cursor.fetchone()

        if str(reaction_allowed) == "None" or str(reaction_allowed) == "(None,)" or str(reaction_allowed[0]) == "enabled":
            pass
        else:
            return

        botuser = self.client.get_user(815328232537718794)

        reactionflag = ['🇦🇸','🇦🇨','🇦🇩','🇦🇪','🇦🇬','🇦🇮','🇦🇱','🇦🇲','🇦🇴','🇦🇶','🇦🇷','🇦🇹','🇦🇺','🇦🇼','🇦🇽','🇦🇿','🇧🇸','🇧🇦','🇧🇧','🇧🇩','🇧🇪','🇧🇫','🇧🇬','🇧🇭','🇧🇮','🇧🇯','🇧🇱','🇧🇲','🇧🇳','🇧🇴','🇧🇶','🇧🇷','🇧🇹','🇧🇻','🇧🇼','🇧🇾','🇧🇿','🇨🇦','🇨🇨','🇨🇩','🇨🇫','🇨🇬','🇨🇭','🇨🇮','🇨🇰','🇨🇱','🇨🇲','🇨🇳','🇨🇴','🇨🇵','🇨🇷','🇨🇺','🇨🇻','🇨🇼','🇨🇽','🇨🇾','🇨🇿','🇩🇪','🇩🇬','🇩🇯','🇩🇰','🇩🇲','🇩🇴','🇩🇿','🇪🇦','🇪🇨','🇪🇪','🇪🇬','🇪🇭','🇪🇷','🇪🇸','🇪🇹','🇪🇺','🇫🇮','🇫🇯','🇫🇰','🇫🇲','🇫🇴','🇫🇷','🇬🇦','🇬🇧','🇬🇩','🇬🇪','🇬🇫','🇬🇬','🇬🇭','🇬🇮','🇬🇱','🇬🇲','🇬🇳','🇬🇵','🇬🇶','🇬🇷','🇬🇸','🇬🇹','🇬🇺','🇬🇼','🇬🇾','🇭🇰','🇭🇲','🇭🇳','🇭🇷','🇭🇹','🇭🇺','🇮🇨','🇮🇩','🇮🇪','🇮🇱','🇮🇲','🇮🇳','🇮🇴','🇮🇶','🇮🇷','🇮🇸','🇮🇹','🇯🇪','🇯🇲','🇯🇴','🇯🇵','🇰🇪','🇰🇬','🇰🇭','🇰🇮','🇰🇲','🇰🇳','🇰🇵','🇰🇷','🇰🇼','🇰🇾','🇰🇿','🇱🇦','🇱🇧','🇱🇨','🇱🇮','🇱🇰','🇱🇷','🇱🇸','🇱🇹','🇱🇺','🇱🇻','🇱🇾','🇲🇦','🇲🇨','🇲🇩','🇲🇪','🇲🇫','🇲🇬','🇲🇭','🇲🇰','🇲🇱','🇲🇲','🇲🇳','🇲🇴','🇲🇵','🇲🇶','🇲🇷','🇲🇸','🇲🇹','🇲🇺','🇲🇻','🇲🇼','🇲🇽','🇲🇾','🇲🇿','🇳🇦','🇳🇨','🇳🇪','🇳🇫','🇳🇬','🇳🇮','🇳🇱','🇳🇴','🇳🇵','🇳🇷','🇳🇺','🇳🇿','🇴🇲','🇵🇦','🇵🇪','🇵🇫','🇵🇬','🇵🇭','🇵🇰','🇵🇱','🇵🇲','🇵🇳','🇵🇷','🇵🇸','🇵🇹','🇵🇼','🇵🇾','🇶🇦','🇷🇪','🇷🇴','🇷🇸','🇷🇺','🇷🇼','🇸🇦','🇸🇧','🇸🇨','🇸🇩','🇸🇪','🇸🇬','🇸🇭','🇸🇮','🇸🇯','🇸🇰','🇸🇱','🇸🇲','🇸🇳','🇸🇴','🇸🇷','🇸🇸','🇸🇹','🇸🇻','🇸🇽','🇸🇾','🇸🇿','🇹🇦','🇹🇨','🇹🇩','🇹🇫','🇹🇬','🇹🇭','🇹🇯','🇹🇰','🇹🇱','🇹🇲','🇹🇳','🇹🇴','🇹🇷','🇹🇹','🇹🇻','🇹🇼','🇹🇿','🇺🇦','🇺🇬','🇺🇲','🇺🇳','🇺🇸','🇺🇾','🇺🇿','🇻🇦','🇻🇨','🇻🇪','🇻🇬','🇻🇮','🇻🇳','🇻🇺','🇼🇫','🇼🇸','🇽🇰','🇾🇪','🇾🇹','🇿🇦','🇿🇲','🇿🇼']

        destinationflag = ['sm','en','ca','ar','en','en','sq','hy','pt','en','es','de','en','nl','sv','az','en','bs','en','bn','fr','fr','bg','ar','fr','fr','fr','en','ms','es','nl','pt','ne','is','en','be','en','en','en','fr','fr','fr','de','fr','mi','es','fr','zh-cn','es','fr','es','es','pt','nl','zh-cn','el','cs','de','en','fr','da','en','es','ar','es','es','et','ar','ar','en','es','am','en','fi','hi','en','en','da','fr','fr','en','en','ka','fr','en','en','en','en','en','fr','fr','fr','el','en','es','en','pt','en','zh-cn','en','es','hr','ht','hu','es','id','ga','iw','en','hi','en','ku','fa','is','it','en','en','ar','ja','sw','ky','km','en','fr','en','ko','ko','ar','en','kk','lo','ar','en','ge','ta','en','en','lt','lb','lv','ar','ar','fr','ro','en','fr','mg','en','mk','fr','my','mn','zh-cn','en','fr','ar','en','mt','en','en','en','es','ms','pt','en','fr','fr','en','en','es','nl','no','ne','en','en','mi','ar','es','es','fr','en','tl','en','pl','fr','en','es','ar','pt','en','es','ar','fr','ro','sr','ru','en','ar','en','fr','ar','sv','ms','en','sl','nl','sk','en','it','fr','so','nl','en','pt','es','nl','ar','en','en','en','fr','fr','fr','th','tg','en','pt','en','ar','en','tr','en','en','zh-cn','sw','uk','sw','en','en','en','es','uz','it','en','es','en','en','vi','fr','fr','sm','sq','ar','fr','af','en','sn']

        if payload.emoji.name in reactionflag:

            LangueIndex = reactionflag.index(payload.emoji.name)

            source = destinationflag[LangueIndex]

            TranslateMessage = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)

            Traduction = trad.translate(text = TranslateMessage.content, dest=source)

            EmbedImpossibleSendDM = discord.Embed(description = "You must to open your DM's to allow me to send you the translate you asked for",
                                                colour = discord.Colour.red())
            EmbedImpossibleSendDM.set_author(name = payload.member,
                                            icon_url = payload.member.avatar_url)

            cursor.execute(f"SELECT yesno FROM DMUser WHERE user_id = {payload.user_id}")
            DMOnOff = cursor.fetchone()

            if Traduction.src == source:

                EmbedSameLanguage = discord.Embed(title="It's the same language",
                                                description = "I don't know why you want to translate a message to the same language as the original one.",
                                                colour = discord.Colour.red())
                EmbedSameLanguage.set_footer(icon_url = f"https://cdn.discordapp.com/avatars/341257685901246466/a_09dadd494a375adaced572682c8ec96c.png?size=4096",
                                            text = f"JeSuisUnBonWhisky#0001")
                EmbedSameLanguage.set_author(icon_url = botuser.avatar_url,
                                            name = botuser)

                try:
                    await TranslateMessage.remove_reaction(emoji = f"{payload.emoji.name}", member = payload.member)
                except discord.Forbidden:
                    pass
                
                if (str(DMOnOff) == "None") or (str(DMOnOff) == "(None,)") :
                    try:
                        await self.client.get_user(payload.user_id).send(embed = EmbedSameLanguage)
                    except discord.Forbidden:
                        await self.client.get_channel(payload.channel_id).send(embed = EmbedImpossibleSendDM)
                else :
                    await self.client.get_channel(payload.channel_id).send(embed = EmbedSameLanguage)
            
            else:
                
                EmbedTranslated = discord.Embed(title = "The translation you requested",
                                                description = f"**Original Message :**\n{TranslateMessage.content}\n\n**Translated Message :**\n{Traduction.text}",
                                                colour = discord.Colour.purple())
                EmbedTranslated.add_field(name = "**__More infos about the message :__**",
                                        value = f"Message link (to directly go to it) : [Click Here]({TranslateMessage.jump_url})\nMessage Channel : <#{TranslateMessage.channel.id}> / **#{TranslateMessage.channel.name}**\nOriginal Message Author : <@{TranslateMessage.author.id}> / **{TranslateMessage.author}**",
                                        inline = False)
                EmbedTranslated.set_footer(icon_url = f"https://cdn.discordapp.com/avatars/341257685901246466/a_09dadd494a375adaced572682c8ec96c.png?size=4096",
                                        text = f"JeSuisUnBonWhisky#0001")
                EmbedTranslated.set_author(icon_url = botuser.avatar_url,
                                        name = botuser)

                try:
                    await TranslateMessage.remove_reaction(emoji = f"{payload.emoji.name}", member = payload.member)
                except discord.Forbidden:
                    pass
                
                if (str(DMOnOff) == "None") or (str(DMOnOff) == "(None,)") :
                    try:
                        await self.client.get_user(payload.user_id).send(embed = EmbedTranslated)
                    except discord.Forbidden:
                        await self.client.get_channel(payload.channel_id).send(embed = EmbedImpossibleSendDM)
                else :
                    await self.client.get_channel(payload.channel_id).send(embed = EmbedTranslated)


def setup(client):
    client.add_cog(ReactionEventSlash(client))
    print("Reaction Language Event cog ready !")
