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
import time

class SupportCommandSlash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name = "support", description = "Need help about anything on the bot ?", guild_ids=[741735273871835197], options=[
        create_option(name="message", description="Message of your problem. Tell me your problem as precisely as possible, please", option_type=3, required=True)
    ])
    async def support(self, ctx : SlashContext, message):

        infojour = time.strftime("%H:%M:%S %d/%m/%Y")

        if ctx.author.guild_permissions.administrator and ctx.guild != None :

            EmbedMessageSent = discord.Embed(title = "Sent !",
                                            description = "Your request has been sent. Check your discord friend invitations.\nThe bot owner will add you as friend if he need it !\nGo check on the [bot owner server](https://discord.gg/gqfFqJp) to know when your support help is done !",
                                            colour = discord.Colour.green()
                                            )
            EmbedMessageSent.add_field(name = "Your message :",
                                    value = f"{message}",
                                    inline = False)
            EmbedMessageSent.add_field(name="Other contact method",
                                    value="mail : contact@unbonwhiskybots.xyz",
                                    inline = False)
            
            EmbedSupportRequest = discord.Embed(title = "Support Required !",
                                                    description = f"**Ticket opened by :**\n``{ctx.author} / {ctx.author.id}``\n\n**Guild :**\n{ctx.guild.name} / {ctx.guild.id}\n\n**Date / Time of the message :**\n{infojour}",
                                                    colour = discord.Colour.red()
                                                    )
            EmbedSupportRequest.add_field(name="Support Message :",
                                        value=f"{message}",
                                        inline=False)
            
            await self.client.get_channel(965009639991287879).send(embed = EmbedSupportRequest)
            await ctx.send(embed = EmbedMessageSent)



def setup(client):
    client.add_cog(SupportCommandSlash(client))
    print("Support Command cog ready !")
