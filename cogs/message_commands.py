from googletrans import RateLimitError
from main import translator_handler

from discord import message_command, IntegrationType, ApplicationContext, Embed
from discord.ext.commands import Cog
import discord

class MessageCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    ########################
    # Translate to english #
    ########################
    
    @message_command(
        name="Translate to english",
        integration_types = {
            IntegrationType.guild_install,
            IntegrationType.user_install,
        }
    )
    @translator_handler
    async def translate_to_english(self, ctx: ApplicationContext, message: discord.Message):
        try :
            trad = await self.bot.trad.translate(message.content, dest='en', src='auto')
        except RateLimitError :
            raise
        except :
            try :
                trad = await self.bot.trad.translate_to_detect(message.content, dest='en', src='auto')
            except RateLimitError :
                raise
            except :
                await ctx.respond("An error occurred.")
                return
        await ctx.respond(f"{trad.text}", ephemeral=True)
    
    
    #######################
    # Translate to french #
    #######################
    
    @message_command(
        name="Translate to french",
        integration_types = {
            IntegrationType.guild_install,
            IntegrationType.user_install,
        }
    )
    @translator_handler
    async def translate_to_french(self, ctx: ApplicationContext, message: discord.Message):
        try :
            trad = await self.bot.trad.translate(message.content, dest='fr', src='auto')
        except RateLimitError :
            raise
        except :
            try :
                trad = await self.bot.trad.translate_to_detect(message.content, dest='fr', src='auto')
            except RateLimitError :
                raise
            except :
                await ctx.respond("An error occurred.")
                return
        await ctx.respond(f"{trad.text}", ephemeral=True)
        
    
    ########################
    # Translate to russian #
    ########################
    
    @message_command(
        name="Translate to russian",
        integration_types = {
            IntegrationType.guild_install,
            IntegrationType.user_install,
        }
    )
    @translator_handler
    async def translate_to_russian(self, ctx: ApplicationContext, message: discord.Message):
        try :
            trad = await self.bot.trad.translate(message.content, dest='ru', src='auto')
        except RateLimitError :
            raise
        except :
            try :
                trad = await self.bot.trad.translate_to_detect(message.content, dest='ru', src='auto')
            except RateLimitError :
                raise
            except :
                await ctx.respond("An error occurred.")
                return
        await ctx.respond(f"{trad.text}", ephemeral=True)
    
    #######################
    # Translate to custom #
    #######################
    
    @message_command(
        name="Translate",
        integration_types = {
            IntegrationType.guild_install,
            IntegrationType.user_install,
        }
    )
    @translator_handler
    async def translate(self, ctx: ApplicationContext, message: discord.Message):
        try :
            trad = await self.bot.trad.translate(message.content, dest=ctx.interaction.locale, src='auto')
        except RateLimitError :
            raise
        except :
            try :
                trad = await self.bot.trad.translate_to_detect(message.content, dest=ctx.interaction.locale, src='auto')
            except RateLimitError :
                raise
            except :
                await ctx.respond("An error occurred.")
                return
        
        EmbedMessage = Embed(
            title = "Translation to your language",
            description = f"Actually, I am doing the translation based on your discord client language setting.\nIt will be possible to change it manually in the future.",
            color = 0x5865F2
        )
        await ctx.respond(f"{trad.text}", embed=EmbedMessage, ephemeral=True)

def setup(bot):
    print("Message Commands are ready !")
    bot.add_cog(MessageCommands(bot))