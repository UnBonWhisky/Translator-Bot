from discord import slash_command, ApplicationContext, AutocompleteContext, option, AutoModActionType, Embed, InteractionContextType, IntegrationType
from discord.ext.commands import Cog
from googletrans import LANGNAMES, RateLimitError
from fnmatch import fnmatch
import flpc
from main import translator_handler

class Translate(Cog):
    def __init__(self, bot):
        self.bot = bot

    #########################
    # autocomplete function #
    #########################

    async def get_languages(ctx: AutocompleteContext):
        filtered_languages = [lang for lang in LANGNAMES if lang.startswith(ctx.value.lower())]
        if len(filtered_languages) > 25:
            return filtered_languages[:25]
        else:
            return filtered_languages
        
    
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
    
    def automod_rules_check(self, automod_rules, Traduction, author, channel):
        
        ban_word = False
        result = {}
        
        for rule in automod_rules:
            if any(role.id in rule.exempt_role_ids for role in author.roles) or (channel.id in rule.exempt_channel_ids) :
                continue
        
            if (type(rule.trigger_metadata.keyword_filter) == list) and (any(AutoModActionType.block_message == action.type for action in rule.actions)) and (not ban_word) :
                for keyword in rule.trigger_metadata.keyword_filter :
                    if fnmatch(Traduction.text, keyword) :
                        ban_word = True

            if (type(rule.trigger_metadata.regex_patterns) == list) and (not ban_word) :
                for keyword in rule.trigger_metadata.regex_patterns :
                    pattern = flpc.compile(keyword)
                    if flpc.fmatch(pattern, Traduction.text) :
                        ban_word = True

            if (type(rule.trigger_metadata.allow_list) == list) and (ban_word) :
                for keyword in rule.trigger_metadata.allow_list :
                    if fnmatch(Traduction.text, keyword) :
                        ban_word = False
                        continue
            
            result.append(rule, ban_word)
        
        for key, value in result.items() :
            if value :
                return key, value
        
        return None, False
        

    #############
    # translate #
    #############
    
    @slash_command(
        name="translate",
        description="Translate a text from a language to another.",
        contexts = {
            InteractionContextType.guild,
            InteractionContextType.private_channel,
            InteractionContextType.bot_dm,
        },
        integration_types = {
            IntegrationType.guild_install,
            IntegrationType.user_install,
        }
    )
    @option(
        name="text",
        description="The text you want to translate.",
        required=True,
        type=str
    )
    @option(
        name="to_language",
        description="The language you want to translate the text into.",
        required=True,
        type=str,
        autocomplete=get_languages
    )
    @option(
        name="from_language",
        description="The language of your actual text.",
        required=False,
        type=str,
        autocomplete=get_languages
    )
    @option(
        name="ephemeral",
        description="if you want the answer to be visible only to you. Default is False",
        required=False,
        type=bool
    )
    @translator_handler
    async def translate(self, ctx : ApplicationContext, text, to_language, from_language = 'auto', ephemeral = False):
        
        await ctx.defer(ephemeral=ephemeral)
        
        try :
            Traduction = await self.bot.trad.translate(text, dest=to_language, src=from_language)
        except RateLimitError :
            raise
        except :
            try :
                Traduction = await self.bot.trad.translate_to_detect(text, dest=to_language, src=from_language)
            except RateLimitError :
                raise
            except :
                await ctx.respond("An error occured while translating the text.\nPlease try again.", ephemeral=ephemeral, delete_after=3 if not ephemeral else None)
                return
            
        if ctx.interaction.context == InteractionContextType.guild :
            try :
                if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_guild :
                    raise Exception
                
                automod_rules = await ctx.guild.fetch_auto_moderation_rules()
                rule, ban_word = await self.bot.loop.run_in_executor(None, self.automod_rules_check, automod_rules, Traduction, ctx.author, ctx.channel)
                
                if ban_word :
                    await ctx.respond("An automod rule have been set up to ban a word you have in the translation.", ephemeral=ephemeral, delete_after=3 if not ephemeral else None)
                    
                    for action in rule.actions :
                        if AutoModActionType.send_alert_message == action.type :
                            alert_channel = await self.bot.fetch_channel(action.metadata.channel_id)
                            
                            EmbedAlert = Embed(title = rule.name,
                                description = f"<@{ctx.author.id}> raised an automod alert when trying to do a translation.",
                                color = 0xff0000
                            )
                            EmbedOriginal = Embed(title = "Original message",
                                description = f"{text}",
                                color = 0xff0000
                            )
                            EmbedTraduction = Embed(title = "Translated message",
                                description = f"{Traduction.text}",
                                color = 0xff0000
                            )
                            
                            await alert_channel.send(embeds = [EmbedAlert, EmbedOriginal, EmbedTraduction])
                    return
            except :
                pass
        
        if len(Traduction.text) > 2000:
            parts = await self.split_message_into_parts(Traduction.text)
            for x in range(len(parts)):
                await ctx.respond(parts[x], ephemeral=ephemeral)
        
        elif len(Traduction.text) == 0:
            await ctx.respond("The translated text is empty.\nI can not translate this.\nIf you think this is not the normal comportment, please open a ticket in the support server", ephemeral=ephemeral)
        
        else :
            try :
                await ctx.respond(f"{Traduction.text}", ephemeral=ephemeral)
            except Exception as e :
                if "Message was blocked by AutoMod" in str(e) :
                    await ctx.respond("The content of the translated has been blocked by Automod.", ephemeral=ephemeral, delete_after=3 if not ephemeral else None)
                else :
                    pass


def setup(bot):
    print("Translate Command is ready !")
    bot.add_cog(Translate(bot))
