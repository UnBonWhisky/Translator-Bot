from discord import Embed, option, ApplicationContext, ChannelType, Permissions, AutocompleteContext
from discord.abc import GuildChannel
from discord.commands import SlashCommandGroup
from discord.ext.commands import Cog
from discord.utils import basic_autocomplete
import aiosqlite

LANGUAGES = ['afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']

class LinkChannels(Cog):
    def __init__(self, bot):
        self.bot = bot

    linkchannels = SlashCommandGroup(
        name="linkchannels", 
        description="Commands used to set a linked translation between 2 channels.",
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
    

    ####################
    # linkchannels add #
    ####################
    
    @linkchannels.command(
        name="add",
        description="Add a translation across 2 channels using a language in each channel.",
    )
    @option(
        name="channel_1",
        description="The first channel where you want to set the link translation",
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
        name="channel_2",
        description="The first channel where you want to set the link translation",
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
    async def linkchannels_add(self, ctx : ApplicationContext, channel_1, channel_2, language_1, language_2):
        
        await ctx.defer(ephemeral=True)

        language_1 = language_1.lower()
        language_2 = language_2.lower()

        if language_1 == language_2 :

            EmbedMessage = Embed(
                description = "You can't set the same language for both languages.",
                color = 0xFF0000
            )
        
        if channel_1 == channel_2 :
                
            EmbedMessage = Embed(
                description = "You can't set the same channel for both channels.",
                color = 0xFF0000
            )
        
        elif (language_1 not in LANGUAGES) or (language_2 not in LANGUAGES) :

            EmbedMessage = Embed(
                description = "One or both of the languages you entered are not available. Please refer to the language list using `/languagelist` command.",
                color = 0xFF0000
            )
        
        else :

            try :
                await channel_1.webhooks()
                await channel_2.webhooks()
            except :
                EmbedMessage = Embed(
                    description = "I need the `Manage Webhooks` permission on both channels to set up the link translation.\nPlease make sure I have the permission globally or for the selected channels and try again.",
                    color = 0xFF0000
                )
                await ctx.respond(embed = EmbedMessage, ephemeral=True)
                return

            await self.bot.cursor.execute(f"SELECT * FROM linkchannels WHERE channel_id_1 = {channel_1.id} OR channel_id_2 = {channel_1.id} OR channel_id_1 = {channel_2.id} OR channel_id_2 = {channel_2.id}")
            LinkChannelsList = await self.bot.cursor.fetchall()

            if LinkChannelsList == []:

                sql = ("INSERT INTO linkchannels(guild_id, channel_id_1, channel_id_2, language_1, language_2) VALUES(?,?,?,?,?)")
                val = (ctx.guild.id, channel_1.id, channel_2.id, language_1, language_2)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()

                EmbedMessage = Embed(
                    description = f"Linked translation between <#{channel_1.id}> : **{language_1}** and <#{channel_2.id}> : **{language_2}** has been setted up.",
                    color=0x5865F2
                )

            else :
                sql = ("DELETE FROM linkchannels WHERE channel_id_1 = ? OR channel_id_2 = ? OR channel_id_1 = ? OR channel_id_2 = ?")
                val = (channel_1.id, channel_1.id, channel_2.id, channel_2.id)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()

                sql = ("INSERT INTO linkchannels(guild_id, channel_id_1, channel_id_2, language_1, language_2) VALUES(?,?,?,?,?)")
                val = (ctx.guild.id, channel_1.id, channel_2.id, language_1, language_2)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()

                EmbedMessage = Embed(
                    description = f"Linked translation between <#{channel_1.id}> : **{language_1}** and <#{channel_2.id}> : **{language_2}** has been setted up.",
                    color=0x5865F2
                )

        await ctx.respond(embed = EmbedMessage, ephemeral=True)
    

    #######################
    # linkchannels remove #
    #######################
        
    @linkchannels.command(
        name="remove",
        description="Remove a link between 2 channels and translation option."
    )
    @option(
        name="channel",
        description="One of the channel where you want to remove the link translation",
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
    async def linkchannels_remove(self, ctx : ApplicationContext, channel):
        
        await ctx.defer(ephemeral=True)

        sql = ("SELECT * FROM linkchannels WHERE guild_id = ? AND (channel_id_1 = ? OR channel_id_2 = ?)")
        val = (ctx.guild.id, channel.id, channel.id)
        await self.bot.cursor.execute(sql, val)
        LinkChannelsList = await self.bot.cursor.fetchall()

        if LinkChannelsList == []:

            EmbedMessage = Embed(
                description = f"No link channels translation has been setted up for <#{channel.id}>\nYou can set it up using `/linkchannels add` command or list existing link channels channels using `/linkchannels list` command.",
                color=0xFF0000
            )

        else :

            sql = ("DELETE FROM linkchannels WHERE guild_id = ? AND (channel_id_1 = ? OR channel_id_2 = ?)")
            val = (ctx.guild.id, channel.id, channel.id)
            await self.bot.cursor.execute(sql, val)
            await self.bot.db.commit()

            EmbedMessage = Embed(
                description = f"Link Channels have been removed for <#{channel.id}>",
                color=0x5865F2
            )

        await ctx.respond(embed = EmbedMessage, ephemeral=True)
    

    #####################
    # linkchannels list #
    #####################
    
    @linkchannels.command(
        name="list",
        description="List all the linked channels in the server."
    )
    async def linkchannels_list(self, ctx : ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        await self.bot.cursor.execute(f"SELECT * FROM linkchannels WHERE guild_id = {ctx.guild.id}")
        LinkChannelsList = await self.bot.cursor.fetchall()

        if LinkChannelsList == []:

            EmbedMessage = Embed(
                description = "No link channels has been setted up in this server",
                color=0xFF0000
            )

        else :

            EmbedMessage = Embed(
                title = "Link Channels list",
                color=0x5865F2
            )

            if len(LinkChannelsList) <= 25:
                for LinkChannels in LinkChannelsList:

                    channel_1 = LinkChannels[1]
                    channel_2 = LinkChannels[2]
                    language_1 = LinkChannels[3]
                    language_2 = LinkChannels[4]
                    EmbedMessage.add_field(
                        name=f"<#{channel_1}> <-> <#{channel_2}>",
                        value=f"{language_1} <-> {language_2}",
                        inline=True
                    )
            else :
                for x in range(24):
                    channel_1 = LinkChannelsList[x][1]
                    channel_2 = LinkChannelsList[x][2]
                    language_1 = LinkChannelsList[x][3]
                    language_2 = LinkChannelsList[x][4]
                    EmbedMessage.add_field(
                        name=f"<#{channel_1}> <-> <#{channel_2}>",
                        value=f"{language_1} <-> {language_2}",
                        inline=True
                    )
                for x in range(24, len(LinkChannelsList)):
                    channel_1 = LinkChannelsList[x][1]
                    channel_2 = LinkChannelsList[x][2]
                    language_1 = LinkChannelsList[x][3]
                    language_2 = LinkChannelsList[x][4]
                    EmbedMessage.description += f"<#{channel_1}> <-> <#{channel_2}> : {language_1} <-> {language_2}\n"

        await ctx.respond(embed = EmbedMessage, ephemeral=True)
        

def setup(bot):
    print("LinkChannels Commands are ready !")
    bot.add_cog(LinkChannels(bot))