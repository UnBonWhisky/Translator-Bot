from discord import Embed, errors
from discord.ext.commands import Cog
from main import ShardedBot

class ReactionEvent(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.LANGUAGES['none'] = 'none'
        self.bot.LANGUAGES['None'] = 'none'
        self.bot.LANGCODES['none'] = 'none'

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

    @ShardedBot.translator_handler
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

        if payload.emoji.name in self.bot.FLAG_CODES.keys() :

            #source = self.destinationflag[self.reactionflag.index(payload.emoji.name)]
            source = self.bot.FLAG_CODES[payload.emoji.name]

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
            
            if Traduction.src == "auto" :
                try :
                    temp_lo = await self.bot.trad.detect(TranslateMessage.content)
                    langue_originale = temp_lo.lang
                except :
                    temp_lo = await self.bot.trad.detect_legacy(TranslateMessage.content)
                    langue_originale = temp_lo.lang
                
                if langue_originale != "auto" :
                    Traduction.src = langue_originale

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
                        flag = self.bot.LANGUAGES[Traduction.src] if Traduction.src != "auto" else "not found"
                        Traduction.text = f"`{flag}` {Traduction.text}"

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
                    EmbedTranslated.description = f"Original message language : {self.bot.LANGUAGES[Traduction.src] if Traduction.src != 'auto' else 'not found'}"

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
