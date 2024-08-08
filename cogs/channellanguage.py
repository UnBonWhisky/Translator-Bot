from discord import Embed, option, ApplicationContext, ChannelType, Permissions, AutocompleteContext
from discord.abc import GuildChannel
from discord.commands import SlashCommandGroup
from discord.ext.commands import Cog
from discord.utils import basic_autocomplete
import aiosqlite

LANGUAGES = ['none','afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']

class ChannelLanguage(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    channellanguage = SlashCommandGroup(
        name="channellanguage", 
        description="Commands used to set a different language as your default language in a specific channel.",
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
    

    ########################
    # channellanguage list #
    ########################

    @channellanguage.command(
        name="list",
        description="Give the different channel languages you set up"
    )
    async def channellanguage_list(self, ctx : ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        # On récupère les données de la table channel_language
        await self.bot.cursor.execute(f"SELECT channel_id, language FROM channel_language WHERE guild_id = {ctx.guild.id}")
        ChannelLanguageList = await self.bot.cursor.fetchall()

        if ChannelLanguageList == []:

            EmbedMessage = Embed(
                description = "I didn't found any different language\nType `/channellanguage add <Channel Mention> <language>` to have a different language in your channel",
                color=0x5865F2
            )

        else :

            EmbedMessage = Embed(
                title= f"{f'{len(ChannelLanguageList)} Different languages found' if len(ChannelLanguageList) > 1 else f'{len(ChannelLanguageList)} Different language found'}",
                description="",
                color = 0x5865F2
            )

            if len(ChannelLanguageList) <= 25: # Si il y a moins de 25 ou 25 channels configurés
                for channel in ChannelLanguageList:

                    EmbedMessage.add_field(
                        name = f"<#{channel[0]}>",
                        value = f"{channel[1]}",
                        inline = True
                    )
            else: # S'il y en a + de 25, alors on met une partie dans les fields et le reste dans la description
                for x in range(24):
                    EmbedMessage.add_field(
                        name = f"<#{ChannelLanguageList[x][0]}>",
                        value = f"{ChannelLanguageList[x][1]}",
                        inline = True
                    )
                for x in range(24, len(ChannelLanguageList)):
                    EmbedMessage.description += f"<#{ChannelLanguageList[x][0]}> : {ChannelLanguageList[x][1]}\n"
                
        await ctx.respond(embed = EmbedMessage, ephemeral=True)


    #######################
    # channellanguage add #
    #######################

    @channellanguage.command(
        name="add",
        description="Add a different channel languages to your server"
    )
    @option(
        name="channel",
        description="Mention channel of the one you want to set a channel language",
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
        name="language",
        description="Language you want to set. Refer to languagelist command to see available languages",
        required=True,
        type=str,
        autocomplete=get_languages
    )
    async def channellanguage_add(self, ctx : ApplicationContext, channel, language):
        
        await ctx.defer(ephemeral=True)

        language = language.lower()

        if language not in LANGUAGES :

            EmbedMessage = Embed(
                description = "I can't translate this language.\nType ``/languagelist`` to know what languages you can use",
                color = 0xff0000
            )

        else :

            await self.bot.cursor.execute(f"SELECT language FROM channel_language WHERE guild_id = {ctx.guild.id} AND channel_id = {channel.id}")
            channelalreadyexist = await self.bot.cursor.fetchone()

            if str(channelalreadyexist) == "None" or str(channelalreadyexist) == "(None,)" :

                sql = ("INSERT INTO channel_language(guild_id, channel_id, language) VALUES(?,?,?)")
                val = (ctx.guild.id, channel.id, language)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()

                EmbedMessage = Embed(
                    description = "Language has been set !",
                    color = 0x00ff00
                )

            else :

                sql = ("UPDATE channel_language SET language = ? WHERE guild_id = ? AND channel_id = ?")
                val = (language, ctx.guild.id, channel.id)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()

                EmbedMessage = Embed(
                    description = "Language has been updated !",
                    color = 0x00ff00
                )

        await ctx.respond(embed = EmbedMessage, ephemeral=True)


    ##########################
    # channellanguage remove #
    ##########################

    @channellanguage.command(
        name="remove",
        description="Remove a different channel languages you set up"
    )
    @option(
        name="channel",
        description="Mention channel of the one you want to remove the channel language",
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
    async def channellanguage_remove(self, ctx : ApplicationContext, channel):
        
        await ctx.defer(ephemeral=True)

        await self.bot.cursor.execute(f"SELECT language FROM channel_language WHERE guild_id = {ctx.guild.id} AND channel_id = {channel.id}")
        ischannelinlist = await self.bot.cursor.fetchone()

        if str(ischannelinlist) == "None" or str(ischannelinlist) == "(None,)" :

            EmbedMessage = Embed(
                description = "This channel has not any different language set !\nPlease give me another channel or type ``/channellanguage list`` to see your different languages setted up.",
                color = 0xff0000
            )

        else :

            await self.bot.cursor.execute(f"DELETE FROM channel_language WHERE guild_id = {ctx.guild.id} AND channel_id = {channel.id}")
            await self.bot.db.commit()

            EmbedMessage = Embed(
                description = "The language of this channel has been deleted !",
                color = 0x00ff00
            )

        await ctx.respond(embed = EmbedMessage, ephemeral=True)


def setup(bot):
    print("Channel Language Commands are ready !")
    bot.add_cog(ChannelLanguage(bot))