from discord import slash_command, ApplicationContext, AutocompleteContext, option
from discord.ext.commands import Cog
from discord.utils import basic_autocomplete
from googletrans import Translator

LANGUAGES = ['afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']

class Translate(Cog):
    def __init__(self, bot):
        self.bot = bot

    #########################
    # autocomplete function #
    #########################

    async def get_languages(ctx: AutocompleteContext):
        filtered_languages = [lang for lang in LANGUAGES if lang.startswith(ctx.value.lower())]
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
    

    #############
    # translate #
    #############
    
    @slash_command(
        name="translate",
        description="Translate a text from a language to another.",
        guild_only=True
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
    async def translate(self, ctx : ApplicationContext, text, to_language, from_language = 'auto', ephemeral = False):
        
        await ctx.defer(ephemeral=ephemeral)
        
        try :
            traduction = await self.bot.trad.translate(text, dest=to_language, src=from_language)
        except :
            try :
                traduction = await self.bot.trad.translate_to_detect(text, dest=to_language, src=from_language)
            except :
                await ctx.respond("An error occured while translating the text.\nPlease try again.", ephemeral=True)
                return
        
        if len(traduction.text) > 2000:
            if ephemeral:
                await ctx.respond("The translated text is too long to be sent in one message.\nEphemeral message is not available for long text.", ephemeral=ephemeral)
            parts = await self.split_message_into_parts(traduction.text)
            for x in range(len(parts)):
                if x == 0 and not ephemeral:
                    await ctx.respond(parts[x])
                else :
                    await ctx.send(parts[x])    
        
        else :
            await ctx.respond(f"{traduction.text}", ephemeral=ephemeral)


def setup(bot):
    print("Translate Command is ready !")
    bot.add_cog(Translate(bot))
