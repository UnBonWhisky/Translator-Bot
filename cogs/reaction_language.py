from discord import Embed, errors
from discord.ext.commands import Cog
import aiosqlite
from googletrans import Translator

class ReactionEvent(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactionflag = ['🇦🇸','🇦🇨','🇦🇩','🇦🇪','🇦🇬','🇦🇮','🇦🇱','🇦🇲','🇦🇴','🇦🇶','🇦🇷','🇦🇹','🇦🇺','🇦🇼','🇦🇽','🇦🇿','🇧🇸','🇧🇦','🇧🇧','🇧🇩','🇧🇪','🇧🇫','🇧🇬','🇧🇭','🇧🇮','🇧🇯','🇧🇱','🇧🇲','🇧🇳','🇧🇴','🇧🇶','🇧🇷','🇧🇹','🇧🇻','🇧🇼','🇧🇾','🇧🇿','🇨🇦','🇨🇨','🇨🇩','🇨🇫','🇨🇬','🇨🇭','🇨🇮','🇨🇰','🇨🇱','🇨🇲','🇨🇳','🇨🇴','🇨🇵','🇨🇷','🇨🇺','🇨🇻','🇨🇼','🇨🇽','🇨🇾','🇨🇿','🇩🇪','🇩🇬','🇩🇯','🇩🇰','🇩🇲','🇩🇴','🇩🇿','🇪🇦','🇪🇨','🇪🇪','🇪🇬','🇪🇭','🇪🇷','🇪🇸','🇪🇹','🇪🇺','🇫🇮','🇫🇯','🇫🇰','🇫🇲','🇫🇴','🇫🇷','🇬🇦','🇬🇧','🇬🇩',' 🇬🇪','🇬🇫','🇬🇬','🇬🇭','🇬🇮','🇬🇱','🇬🇲','🇬🇳','🇬🇵','🇬🇶','🇬🇷','🇬🇸','🇬🇹','🇬🇺','🇬🇼','🇬🇾','🇭🇰',' 🇭🇲','🇭🇳','🇭🇷','🇭🇹','🇭🇺','🇮🇨','🇮🇩','🇮🇪','🇮🇱','🇮🇲','🇮🇳','🇮🇴','🇮🇶','🇮🇷','🇮🇸','🇮🇹','🇯🇪',' 🇯🇲','🇯🇴','🇯🇵','🇰🇪','🇰🇬','🇰🇭','🇰🇮','🇰🇲','🇰🇳','🇰🇵','🇰🇷','🇰🇼','🇰🇾','🇰🇿','🇱🇦','🇱🇧','🇱🇨',' 🇱🇮','🇱🇰','🇱🇷','🇱🇸','🇱🇹','🇱🇺','🇱🇻','🇱🇾','🇲🇦','🇲🇨','🇲🇩','🇲🇪','🇲🇫','🇲🇬','🇲🇭','🇲🇰','🇲🇱',' 🇲🇲','🇲🇳','🇲🇴','🇲🇵','🇲🇶','🇲🇷','🇲🇸','🇲🇹','🇲🇺','🇲🇻','🇲🇼','🇲🇽','🇲🇾','🇲🇿','🇳🇦','🇳🇨','🇳🇪',' 🇳🇫','🇳🇬','🇳🇮','🇳🇱','🇳🇴','🇳🇵','🇳🇷','🇳🇺','🇳🇿','🇴🇲','🇵🇦','🇵🇪','🇵🇫','🇵🇬','🇵🇭','🇵🇰','🇵🇱',' 🇵🇲','🇵🇳','🇵🇷','🇵🇸','🇵🇹','🇵🇼','🇵🇾','🇶🇦','🇷🇪','🇷🇴','🇷🇸','🇷🇺','🇷🇼','🇸🇦','🇸🇧','🇸🇨','🇸🇩',' 🇸🇪','🇸🇬','🇸🇭','🇸🇮','🇸🇯','🇸🇰','🇸🇱','🇸🇲','🇸🇳','🇸🇴','🇸🇷','🇸🇸','🇸🇹','🇸🇻','🇸🇽','🇸🇾','🇸🇿',' 🇹🇦','🇹🇨','🇹🇩','🇹🇫','🇹🇬','🇹🇭','🇹🇯','🇹🇰','🇹🇱','🇹🇲','🇹🇳','🇹🇴','🇹🇷','🇹🇹','🇹🇻','🇹🇼','🇹🇿',' 🇺🇦','🇺🇬','🇺🇲','🇺🇳','🇺🇸','🇺🇾','🇺🇿','🇻🇦','🇻🇨','🇻🇪','🇻🇬','🇻🇮','🇻🇳','🇻🇺','🇼🇫','🇼🇸','🇽🇰',' 🇾🇪','🇾🇹','🇿🇦','🇿🇲','🇿🇼','🇺🇦','🇸🇪','🏴󠁧󠁢󠁥󠁮󠁧󠁿','🏴󠁧󠁢󠁷󠁬󠁳󠁿']
        self.destinationflag = ['sm','en','ca','ar','en','en','sq','hy','pt','en','es','de','en','nl','sv','az','en','bs','en','bn','fr','fr','bg','ar','fr','fr','fr','en','ms','es','nl','pt','ne','is','en','be','en','en','en','fr','fr','fr','de','fr','mi','es','fr','zh-cn','es','fr','es','es','pt','nl','zh-cn','el','cs','de','en','fr','da','en','es','ar','es','es','et','ar','ar','en','es','am','en','fi','hi','en','en','da','fr','fr','en','en','ka','fr','en','en','en','en','en','fr','fr','fr','el','en','es','en','pt','en','zh-cn','en','es','hr','ht','hu','es','id','ga','iw','en','hi','en','ku','fa','is','it','en','en','ar','ja','sw','ky','km','en','fr','en','ko','ko','ar','en','kk','lo','ar','en','ge','ta','en','en','lt','lb','lv','ar','ar','fr','ro','en','fr','mg','en','mk','fr','my','mn','zh-cn','en','fr','ar','en','mt','en','en','en','es','ms','pt','en','fr','fr','en','en','es','nl','no','ne','en','en','mi','ar','es','es','fr','en','tl','en','pl','fr','en','es','ar','pt','en','es','ar','fr','ro','sr','ru','en','ar','en','fr','ar','sv','ms','en','sl','nl','sk','en','it','fr','so','nl','en','pt','es','nl','ar','en','en','en','fr','fr','fr','th','tg','en','pt','en','ar','en','tr','en','en','zh-cn','sw','uk','sw','en','en','en','es','uz','it','en','es','en','en','vi','fr','fr','sm','sq','ar','fr','af','en','sn','uk','sv','en','cy']
        
    ########################################################
    # Fonction pour créer un embed avec des champs divisés #
    ########################################################
    
    async def create_embed_with_fields(self, content, title, color=0x5865F2):
        embed = Embed(title=title, color=color)
        fields = 0
        while content:
            # Trouver la position du dernier espace dans les 1024 premiers caractères
            if len(content) > 1024:
                fields += 1
                last_space = content[:1024].rfind(" ")
                if last_space != -1:
                    # Si un espace est trouvé, diviser le contenu à cet espace
                    part, content = content[:last_space], content[last_space+1:]
                else:
                    # Si aucun espace n'est trouvé, couper simplement à 1024 caractères
                    part, content = content[:1024], content[1024:]
            else:
                part, content = content, ""
            
            if fields == 0:
                embed.description = part
            else :
                # Ajouter le morceau de texte comme un nouveau champ dans l'embed
                embed.add_field(name="\u200b", value=part, inline=False)

        return embed
    
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

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member is None :
            return

        if (payload.guild_id is None) or (payload.member.bot is True):
            return
        
        cursor = await self.bot.db.cursor()
        
        await cursor.execute(f"SELECT reaction_activated FROM default_guild_language WHERE guild_id = {payload.guild_id}")
        reaction_allowed = await cursor.fetchone()

        if str(reaction_allowed) == "None" or str(reaction_allowed) == "(None,)" or str(reaction_allowed[0]) == "enabled":
            pass
        else:
            await cursor.close()
            return
        

        await cursor.execute(f"SELECT forced FROM force_reaction WHERE guild_id = {payload.guild_id}")
        forced = await cursor.fetchone()

        if str(forced) == "None" or str(forced) == "(None,)" or forced[0] == "none":
            DMOnOff = None
        elif forced[0] == "DM":
            DMOnOff = "None"
        elif forced[0] == "channel":
            DMOnOff = "channel"
            
        
        await cursor.execute(f"SELECT minimalist FROM force_reaction WHERE guild_id = {payload.guild_id}")
        minimalist = await cursor.fetchone()
        
        if str(minimalist) == "None" or str(minimalist) == "(None,)":
            minimalist = None
        else :
            minimalist = "yes"
            
        await cursor.execute(f"SELECT timeout FROM force_reaction WHERE guild_id = {payload.guild_id}")
        timeout = await cursor.fetchone()
        
        if str(timeout) == "None" or str(timeout) == "(None,)":
            timeout = None
        else :
            timeout = int(timeout[0])

        if payload.emoji.name in self.reactionflag:

            source = self.destinationflag[self.reactionflag.index(payload.emoji.name)]

            TranslateMessage = self.bot.get_message(payload.message_id)
            if TranslateMessage is None:
                try :
                    TranslateMessage = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                except (errors.Forbidden, errors.ApplicationCommandInvokeError) :
                    await cursor.close()
                    return

            MessageAuthor = TranslateMessage.author

            try :
                Traduction = await self.bot.trad.translate(text = TranslateMessage.content, dest=source)
            except :
                try :
                    Traduction = await self.bot.trad.translate_to_detect(text = TranslateMessage.content, dest=source)
                except :
                    await cursor.close()
                    return

            EmbedImpossibleSendDM = Embed(
                description = "You must to open your DM's to allow me to send you the translate you asked for",
                color = 0xff0000
            )
            EmbedImpossibleSendDM.set_author(
                name = payload.member.display_name,
                icon_url = payload.member.avatar.url if payload.member.avatar is not None else "https://cdn.pfps.gg/pfps/4909-default-discord.png"
            )

            if DMOnOff is None :
                await cursor.execute(f"SELECT yesno FROM DMUser WHERE user_id = {payload.user_id}")
                DMOnOff = await cursor.fetchone()

            if Traduction.src == source:

                EmbedSameLanguage = Embed(
                    title="It's the same language",
                    description = "I don't know why you want to translate a message to the same language as the original one.",
                    color = 0xff0000
                )
                EmbedSameLanguage.set_author(
                    name = payload.member.display_name,
                    icon_url = payload.member.avatar.url if payload.member.avatar is not None else "https://cdn.pfps.gg/pfps/4909-default-discord.png"
                )
                EmbedSameLanguage.set_author(
                    name = MessageAuthor.display_name,
                    icon_url = MessageAuthor.avatar.url if MessageAuthor.avatar is not None else "https://cdn.pfps.gg/pfps/4909-default-discord.png"
                )

                try:
                    await TranslateMessage.remove_reaction(emoji = f"{payload.emoji.name}", member = payload.member)
                except :
                    pass

                if (str(DMOnOff) == "None") or (str(DMOnOff) == "(None,)") :
                    try:
                        SendRequest = await self.bot.fetch_user(payload.user_id)
                        await SendRequest.send(embed = EmbedSameLanguage)
                    except errors.Forbidden:
                        try :
                            await self.bot.get_channel(payload.channel_id).send(embed = EmbedImpossibleSendDM)
                        except:
                            pass
                else :
                    try :
                        await self.bot.get_channel(payload.channel_id).send(embed = EmbedSameLanguage)
                    except :
                        pass

            else:

                LANGUAGES = [None, 'None', 'none','afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']
                LANGUAGESEXT = ['none', 'none', 'none','af','sq','am','ar','hy','az','eu','be','bn','bs','bg','ca','ceb','ny','zh-cn','zh-tw','co','hr','cs','da','nl','en','eo','et','tl','fi','fr','fy','gl','ka','de','el','gu','ht','ha','haw','iw','he','hi','hmn','hu','is','ig','id','ga','it','ja','jw','kn','kk','km','ko','ku','ky','lo','la','lv','lt','lb','mk','mg','ms','ml','mt','mi','mr','mn','my','ne','no','or','ps','fa','pl','pt','pa','ro','ru','sm','gd','sr','st','sn','sd','si','sk','sl','so','es','su','sw','sv','tg','ta','te','th','tr','uk','ur','ug','uz','vi','cy','xh','yi','yo','zu']

                await cursor.execute(f"SELECT info FROM langinfo WHERE guild_id = {payload.guild_id}")
                langinfo = await cursor.fetchone()
                if str(langinfo) != "None" :
                    langinfo = langinfo[0]
                
                if minimalist == "yes" and (str(DMOnOff) == "channel" or str(DMOnOff) == "('1',)") :
                    try:
                        await TranslateMessage.remove_reaction(emoji = f"{payload.emoji.name}", member = payload.member)
                    except :
                        pass

                    if langinfo == "enabled" :
                        flag = LANGUAGES[LANGUAGESEXT.index(Traduction.src.lower())]
                        Traduction.text = f"`{flag.lower()}` {Traduction.text}"

                    if len(Traduction.text) > 2000 :
                        parts = await self.split_message_into_parts(Traduction.text)
                        for x in range(len(parts)) :
                            if x == 0 :
                                await TranslateMessage.reply(content=parts[x], mention_author=False, delete_after = timeout)
                            else :
                                await self.bot.get_channel(payload.channel_id).send(content=parts[x], delete_after = timeout)
                    else :
                        try:
                            await TranslateMessage.reply(content=Traduction.text, mention_author=False, delete_after = timeout)
                        except :
                            pass
                    await cursor.close()
                    return
                    

                EmbedTranslated = Embed(
                    title = "The translation you requested",
                    color = 0x5865F2
                )

                if str(langinfo) != "None" :
                    EmbedTranslated.description = f"Original message language : {LANGUAGES[LANGUAGESEXT.index(Traduction.src.lower())]}"

                Embeds = [EmbedTranslated]
                content = await self.create_embed_with_fields(TranslateMessage.content, "**Original Message :**")
                Embeds.append(content)
                
                content = await self.create_embed_with_fields(Traduction.text, "**Translated Message :**")
                Embeds.append(content)

                EmbedInfos = Embed(color=0x5865F2)
                EmbedInfos.add_field(
                    name = "**__More infos about the message :__**",
                    value = f"Message link (to directly go to it) : [Click Here]({TranslateMessage.jump_url})\nMessage Channel : <#{TranslateMessage.channel.id}> / **#{TranslateMessage.channel.name}**\nOriginal Message Author : <@{TranslateMessage.author.id}> / **{TranslateMessage.author}**",
                    inline = False
                )
                EmbedInfos.set_footer(
                    icon_url = payload.member.avatar.url if payload.member.avatar is not None else "https://cdn.pfps.gg/pfps/4909-default-discord.png",
                    text = payload.member.display_name
                )

                EmbedTranslated.set_author(
                    name = MessageAuthor.display_name,
                    icon_url = MessageAuthor.avatar.url if MessageAuthor.avatar is not None else "https://cdn.pfps.gg/pfps/4909-default-discord.png"
                )

                Embeds.append(EmbedInfos)

                try:
                    await TranslateMessage.remove_reaction(emoji = f"{payload.emoji.name}", member = payload.member)
                except :
                    pass

                if (str(DMOnOff) == "None") or (str(DMOnOff) == "(None,)") :
                    try:
                        SendRequest = await self.bot.fetch_user(payload.user_id)
                        if (len(Traduction.text) + len(TranslateMessage.content)) > 5500 :
                            await SendRequest.send(embeds = [Embeds[0], Embeds[1]])
                            await SendRequest.send(embeds = [Embeds[2], Embeds[3]])
                            await cursor.close()
                            return
                        else :
                            await SendRequest.send(embeds = Embeds)
                            await cursor.close()
                            return
                    except errors.Forbidden :
                        try :
                            await self.bot.get_channel(payload.channel_id).send(embed = EmbedImpossibleSendDM, delete_after = timeout)
                            await cursor.close()
                            return
                        except:
                            await cursor.close()
                            pass
                else :
                    try:
                        if (len(Traduction.text) + len(TranslateMessage.content)) > 5500 :
                            await self.bot.get_channel(payload.channel_id).send(embeds = [Embeds[0], Embeds[1]], delete_after = timeout)
                            await self.bot.get_channel(payload.channel_id).send(embeds = [Embeds[2], Embeds[3]], delete_after = timeout)
                            await cursor.close()
                            return
                        else :
                            await self.bot.get_channel(payload.channel_id).send(embeds = Embeds, delete_after = timeout)
                            await cursor.close()
                            return
                    except :
                        await cursor.close()
                        pass


def setup(bot):
    print("Reaction Language is ready !")
    bot.add_cog(ReactionEvent(bot))
