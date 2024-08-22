from discord import Embed, ApplicationContext, slash_command, default_permissions, InteractionContextType
from discord.ext.commands import Cog

class LanguageList(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "languagelist",
        description = "Command for servers admins. Language list supported by the bot",
        contexts={InteractionContextType.guild}
    )
    @default_permissions(administrator=True)
    async def languagelist(self, ctx : ApplicationContext):
        
        await ctx.defer(ephemeral=True)
        
        LanguesDispos = {}
        for language in self.bot.LANG_NAMES:
            if LanguesDispos.get(language[0]) is None:
                LanguesDispos[language[0]] = [language]
            else:
                LanguesDispos[language[0]].append(language)
        
        for letter in LanguesDispos:
            LanguesDispos[letter] = "\n".join(LanguesDispos[letter])

        EmbedListLanguages = Embed(
            title = f"Available languages to translate ({len(self.bot.LANG_NAMES)} languages)",
            description = "You can set `none` to a `/channellanguage` to set it as a channel without any translation\n",
            color = 0x5865F2
        )

        for letter in LanguesDispos:
            if letter == "a":
                EmbedListLanguages.description += f"\n**{letter.upper()}**\n{LanguesDispos[letter]}"
            else:
                EmbedListLanguages.add_field(
                    name = letter.upper(),
                    value = f"{LanguesDispos[letter]}",
                    inline = True
                )

        await ctx.respond(embed = EmbedListLanguages, ephemeral=True)


def setup(bot):
    print("Language List Command is ready !")
    bot.add_cog(LanguageList(bot))