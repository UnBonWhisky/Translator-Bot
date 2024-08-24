from googletrans import RateLimitError
from main import translator_handler

from discord import message_command, IntegrationType, ApplicationContext, Embed
from discord.ext.commands import Cog
import discord

class MessageCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def split_message_into_parts(self, message, max_length=2000):
        parts = []
        while len(message) > max_length:
            # Trouver la position du dernier espace avant la limite max_length
            last_space = message.rfind(' ', 0, max_length)
            if last_space != -1:
                # Couper le message au dernier espace
                parts.append(message[:last_space])
                message = message[last_space+1:]
            else:
                # Si aucun espace n'est trouvé, couper au caractère max_length
                parts.append(message[:max_length])
                message = message[max_length:]
        # Ajouter le reste du message s'il en reste
        if message:
            parts.append(message)
        return parts
    
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
            
        if len(trad.text) > 2000:
            parts = await self.split_message_into_parts(trad.text)
            for part in parts:
                await ctx.respond(f"{part}", ephemeral=True)
        else :
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
        
        if len(trad.text) > 2000:
            parts = await self.split_message_into_parts(trad.text)
            for part in parts:
                await ctx.respond(f"{part}", ephemeral=True)
        else :
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
        
        if len(trad.text) > 2000:
            parts = await self.split_message_into_parts(trad.text)
            for part in parts:
                await ctx.respond(f"{part}", ephemeral=True)
        else :
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
        if len(trad.text) > 2000:
            parts = await self.split_message_into_parts(trad.text)
            for part in parts:
                if part == parts[-1]:
                    await ctx.respond(f"{part}", embed=EmbedMessage, ephemeral=True)
                else :
                    await ctx.respond(f"{part}", ephemeral=True)
        else :
            await ctx.respond(f"{trad.text}", embed=EmbedMessage, ephemeral=True)

def setup(bot):
    print("Message Commands are ready !")
    bot.add_cog(MessageCommands(bot))