from discord import Embed, ApplicationContext, slash_command, default_permissions
from discord.ext.commands import Cog

class LanguageList(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "languagelist",
        description = "Command for servers admins. Language list supported by the bot",
        guild_only=True
    )
    @default_permissions(administrator=True)
    async def languagelist(self, ctx : ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        LANGUAGES = ['afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']

        LanguesDispos = {}
        for language in LANGUAGES:
            if LanguesDispos.get(language[0]) is None:
                LanguesDispos[language[0]] = [language]
            else:
                LanguesDispos[language[0]].append(language)
        
        for letter in LanguesDispos:
            LanguesDispos[letter] = "\n".join(LanguesDispos[letter])

        EmbedListLanguages = Embed(
            title = "Available languages to translate",
            description = "You can set `none` to a channel language to set it as a channel without any translation\n(f.e : channel allowed to speak with multiple languages in it)",
            color = 0x5865F2
        )

        for letter in LanguesDispos:
            EmbedListLanguages.add_field(name = letter.upper(),
                                        value = f"{LanguesDispos[letter]}",
                                        inline = True)

        await ctx.respond(embed = EmbedListLanguages, ephemeral=True)


def setup(bot):
    print("Language List Command is ready !")
    bot.add_cog(LanguageList(bot))