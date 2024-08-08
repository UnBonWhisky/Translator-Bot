from discord import Embed, option, ApplicationContext, Permissions, AutocompleteContext
from discord.commands import SlashCommandGroup
from discord.ext.commands import Cog
from discord.utils import basic_autocomplete
import aiosqlite

LANGUAGES = ['afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']

class DefaultLanguage(Cog):
    def __init__(self, bot):
        self.bot = bot

    defaultlanguage = SlashCommandGroup(
        name="defaultlanguage", 
        description="Commands used to set or remove a default language for the server.",
        guild_only=True,
        default_member_permissions=Permissions(administrator=True)
    )
    

    #########################
    # autocomplete function #
    #########################

    async def get_languages(ctx: AutocompleteContext):
        filtered_languages = [lang for lang in LANGUAGES if lang.startswith(ctx.value.lower())]
        if len(filtered_languages) > 25:
            return filtered_languages[:25]
        else:
            return filtered_languages


    #######################
    # defaultlanguage set #
    #######################

    @defaultlanguage.command(
        name="set",
        description="Used to set a default language for the server (1 for the full server)",
        dm_permission=False
    )
    @option(
        name="language",
        description="Language you want to set. Refer to languagelist to see available languages.",
        required=True,
        type=str,
        autocomplete=get_languages
    )
    async def defaultlanguage_set(self, ctx : ApplicationContext, language):
        
        await ctx.defer(ephemeral=True)

        language = language.lower()

        await self.bot.cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
        DefaultLG = await self.bot.cursor.fetchone()

        if language in LANGUAGES :

            if str(DefaultLG) == "None" :

                sql = ("INSERT INTO default_guild_language(guild_id, default_language) VALUES(?,?)")
                val = (ctx.guild.id, language)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()

                EmbedLanguage = Embed(
                    description = "Default Language set !",
                    color = 0x00ff00
                )

            else :

                sql = ("UPDATE default_guild_language SET default_language = ? WHERE guild_id = ?")
                val = (language, ctx.guild.id)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()

                EmbedLanguage = Embed(
                    description = "Default Language updated !",
                    color = 0x00ff00
                )

        else :

            EmbedLanguage = Embed(
                description = "I can't translate to this language.\nType `/languagelist` to have the full language list",
                color = 0xff0000
            )

        await ctx.respond(embed = EmbedLanguage, ephemeral=True)


    #########################
    # defaultlanguage reset #
    #########################

    @defaultlanguage.command(
        name="reset",
        description="Used to remove the default language of the server"
    )
    async def defaultlanguage_reset(self, ctx: ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        await self.bot.cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
        DefaultLG = await self.bot.cursor.fetchone()

        if str(DefaultLG) == "None" or str(DefaultLG) == "(None,)":

            EmbedDeleted = Embed(
                description = "You didn't put any default language before",
                color = 0xff0000
            )

        else:

            await self.bot.cursor.execute(f"DELETE FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
            await self.bot.db.commit()

            EmbedDeleted = Embed(
                description = "Default Language has been deleted !",
                color = 0x00ff00
            )

        await ctx.respond(embed = EmbedDeleted, ephemeral=True)


    #######################
    # defaultlanguage see #
    #######################

    @defaultlanguage.command(
        name="see",
        description="Used to see the default language of the server"
    )
    async def defaultlanguage_see(self, ctx: ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        await self.bot.cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
        DefaultLG = await self.bot.cursor.fetchone()

        if str(DefaultLG) == "None" or str(DefaultLG) == "(None,)":

            EmbedNone = Embed(
                title="You didn't have a default language before this command.",
                description= "You can use `/defaultlanguage set <language in the languagelist command>` to set a default language for the server.",
                color = 0xff0000
            )

        else:

            EmbedNone = Embed(
                title = "Here is your default language :",
                description = f"{DefaultLG[0]}",
                color = 0x5865F2
            )

        await ctx.respond(embed = EmbedNone, ephemeral=True)


def setup(bot):
    print("Default Language Commands are ready !")
    bot.add_cog(DefaultLanguage(bot))