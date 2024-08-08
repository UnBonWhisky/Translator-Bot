from discord import Embed, option, ApplicationContext, ChannelType, Permissions, AutocompleteContext
from discord.abc import GuildChannel
from discord.commands import SlashCommandGroup
from discord.ext.commands import Cog
from discord.utils import basic_autocomplete
import aiosqlite

LANGUAGES = ['afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']

class ReverseLanguages(Cog):
    def __init__(self, bot):
        self.bot = bot

    reverse = SlashCommandGroup(
        name="reverse", 
        description="Commands used to set a reversed translation between two languages.",
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
    

    ################
    # reverse add #
    ################
    
    @reverse.command(
        name="add",
        description="Add a reversed option between two languages in a specific channel."
    )
    @option(
        name="channel",
        description="The channel where you want to set the reverse translation",
        required=True,
        type=GuildChannel,
        channel_types=[
            ChannelType.text,
            ChannelType.voice,
            ChannelType.stage_voice,
            ChannelType.news,
            ChannelType.forum
        ]
    )
    @option(
        name="language_1",
        description="The first language that will be translated into the second language",
        required=True,
        opt_type=str,
        autocomplete=get_languages
    )
    @option(
        name="language_2",
        description="The second language that will be translated into the first language",
        required=True,
        opt_type=str,
        autocomplete=get_languages
    )
    async def reverse_add(self, ctx : ApplicationContext, channel, language_1, language_2):
        
        await ctx.defer(ephemeral=True)

        language_1 = language_1.lower()
        language_2 = language_2.lower()

        if language_1 == language_2 :

            EmbedMessage = Embed(
                description = "You can't set the same language for both languages.",
                color = 0xFF0000
            )
        
        elif (language_1 not in LANGUAGES) or (language_2 not in LANGUAGES) :

            EmbedMessage = Embed(
                description = "One or both of the languages you entered are not available. Please refer to the language list using `/languagelist` command.",
                color = 0xFF0000
            )
        
        else :

            await self.bot.cursor.execute(f"SELECT * FROM reversed WHERE guild_id = {ctx.guild.id} AND channel_id = {channel.id}")
            ReversedLanguagesList = await self.bot.cursor.fetchall()

            if ReversedLanguagesList == []:

                sql = ("INSERT INTO reversed(guild_id, channel_id, language_1, language_2) VALUES(?,?,?,?)")
                val = (ctx.guild.id, channel.id, language_1, language_2)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()

                EmbedMessage = Embed(
                    description = f"Reversed translation between **{language_1}** and **{language_2}** has been setted up in <#{channel.id}>",
                    color=0x5865F2
                )

            else :

                sql = ("UPDATE reversed SET language_1 = ?, language_2 = ? WHERE guild_id = ? AND channel_id = ?")
                val = (language_1, language_2, ctx.guild.id, channel.id)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()

                EmbedMessage = Embed(
                    description = f"Reversed translation between **{language_1}** and **{language_2}** has been updated in <#{channel.id}>",
                    color=0x5865F2
                )

        await ctx.respond(embed = EmbedMessage, ephemeral=True)
    

    ###################
    # reverse remove #
    ###################
        
    @reverse.command(
        name="remove",
        description="Remove a reversed option between two languages in a specific channel."
    )
    @option(
        name="channel",
        description="The channel where you want to remove the reversed translation",
        required=True,
        type=GuildChannel,
        channel_types=[
            ChannelType.text,
            ChannelType.voice,
            ChannelType.stage_voice,
            ChannelType.news,
            ChannelType.forum
        ]
    )
    async def reverse_remove(self, ctx : ApplicationContext, channel):
        
        await ctx.defer(ephemeral=True)

        sql = ("SELECT * FROM reversed WHERE guild_id = ? AND channel_id = ?")
        val = (ctx.guild.id, channel.id)
        await self.bot.cursor.execute(sql, val)
        ReversedLanguagesList = await self.bot.cursor.fetchall()

        if ReversedLanguagesList == []:

            EmbedMessage = Embed(
                description = f"No reversed translation has been setted up for <#{channel.id}>\nYou can set it up using `/reversed add` command or list existing reversed channels using `/reverse list` command.",
                color=0xFF0000
            )

        else :

            sql = ("DELETE FROM reversed WHERE guild_id = ? AND channel_id = ?")
            val = (ctx.guild.id, channel.id)
            await self.bot.cursor.execute(sql, val)
            await self.bot.db.commit()

            EmbedMessage = Embed(
                description = f"Reversed translation has been removed in <#{channel.id}>",
                color=0x5865F2
            )

        await ctx.respond(embed = EmbedMessage, ephemeral=True)
    

    #################
    # reverse list #
    #################
    @reverse.command(
        name="list",
        description="List all the reversed options in the server."
    )
    async def reverse_list(self, ctx : ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        await self.bot.cursor.execute(f"SELECT * FROM reversed WHERE guild_id = {ctx.guild.id}")
        ReversedLanguagesList = await self.bot.cursor.fetchall()

        if ReversedLanguagesList == []:

            EmbedMessage = Embed(
                description = "No reversed translation has been setted up in this server",
                color=0xFF0000
            )

        else :

            EmbedMessage = Embed(
                title = "Reversed translation list",
                color=0x5865F2
            )

            for ReversedLanguages in ReversedLanguagesList:

                channel = ReversedLanguages[1]
                language_1 = ReversedLanguages[2]
                language_2 = ReversedLanguages[3]
                EmbedMessage.add_field(
                    name=f"<#{channel}>",
                    value=f"{language_1} <-> {language_2}",
                    inline=True
                )

        await ctx.respond(embed = EmbedMessage, ephemeral=True)
        

def setup(bot):
    print("Reverse Commands are ready !")
    bot.add_cog(ReverseLanguages(bot))