from discord import Thread, Webhook, errors
from discord.ext.commands import Cog

import re, aiohttp
from difflib import SequenceMatcher

# Connexion au service de traduction google translate

class MessageTranslator(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_url(self, input_string):
        pattern = r'^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})$'
        if re.match(pattern, input_string):
            return True
        else:
            return False
    
    async def is_emoji_or_mention(self, input_string):
        pattern = r'^<[^ ]+>$'
        if re.match(pattern, input_string):
            return True
        else:
            return False

    async def returnmessage(self, texte):
        # On récupère le contenu du message
        MessageEmojis = texte
        if "\n" in MessageEmojis: # Si le message contient des retours à la ligne, on les supprime
            MessageEmojis = re.findall(r'\S+|\n',MessageEmojis)

        else: # Sinon, on supprime les espaces inutiles
            MessageEmojis = " ".join(MessageEmojis.split())
            MessageEmojis = MessageEmojis.split()
        Mots_A_Supprimer = []

        # On supprime les espaces inutiles
        for No_Spaces in range(len(MessageEmojis)):
            if MessageEmojis[No_Spaces] == '':
                Mots_A_Supprimer.append(No_Spaces)

        # On supprime les mots qui sont des emojis
        for x in range(len(Mots_A_Supprimer)):
            del(MessageEmojis[Mots_A_Supprimer[x]])

        Mots_A_Supprimer = []

        # On récupère les mots qui sont des channels ou des mentions
        for word in range(len(MessageEmojis)):
            result = await self.is_emoji_or_mention(MessageEmojis[word])
            if result :
                Mots_A_Supprimer.append(word)

        # On supprime les mots qui sont des channels ou des mentions
        for x in range(len(Mots_A_Supprimer))[::-1]:
            del(MessageEmojis[Mots_A_Supprimer[x]])

        try: # On tente de joindre les mots
            MessageEmojis = ' '.join(MessageEmojis)
        except Exception:
            MessageEmojis = None
        
        return MessageEmojis
    
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
    
    async def is_custom_emoji(self, original_message, translated_message):
        # On récupère les emojis du message original
        emojis_original = re.findall(r'(<(a:|:)\w+:\d+>)', original_message)
        emojis_translated = re.findall(r'(<(a?[:：][^<>]*[:：](\d+))>)', translated_message)
        for x in range(len(emojis_original)):
            emojis_original[x] = emojis_original[x][0]
        for x in range(len(emojis_translated)):
            emojis_translated[x] = emojis_translated[x][0]

        for emoji_original in emojis_original:
            emoji_id = emoji_original.split(':')[-1]

            for emoji_translated in emojis_translated :
                if emoji_id in emoji_translated:
                    translated_message = translated_message.replace(emoji_translated, emoji_original)
        
        return translated_message
    
    def compare_messages(self, original_message, translated_message):
        original_normalized = re.sub(r'\s+', '', original_message).lower()
        translated_normalized = re.sub(r'\s+', '', translated_message).lower()
        
        if original_normalized == translated_normalized:
            return True
        
        # Utiliser SequenceMatcher pour évaluer la similarité entre les chaînes
        ratio = SequenceMatcher(None, original_normalized, translated_normalized).ratio()
        return ratio >= 0.75

    @Cog.listener()
    async def on_message(self, message):

        self.bot.LANGUAGES['none'] = 'none'
        self.bot.LANGUAGES['None'] = 'none'
        self.bot.LANGCODES['none'] = 'none'
        
        is_url = await self.is_url(message.content)
        is_emoji_or_mention = await self.is_emoji_or_mention(message.content)

        # Si l'auteur du message est un bot ou le message vient d'un MP, on ne fait rien
        if (message.author.bot is True) or (message.guild is None) or (is_emoji_or_mention) :
            return

        # On retire les caractères spéciaux du message pour un test de traduction basé sur la séquence
        MessageOnly = ''.join(item for item in message.content if item.isalnum())

        if type(message.channel) is Thread: # Si le message est envoyé dans un thread, on récupère le channel de base
            channel_id = message.channel.parent_id
        else : # Sinon, on récupère le channel actuel
            channel_id = message.channel.id

        cursor = await self.bot.db.cursor()

        await cursor.execute(f"SELECT channel_id_1, channel_id_2, language_1, language_2, webhook_1, webhook_2 FROM linkchannels WHERE guild_id = {message.guild.id} AND (channel_id_1 = {channel_id} OR channel_id_2 = {channel_id})")
        result = await cursor.fetchone()
        if result is not None :
            result = list(result)
            if result[0] is None :
                result = None
        
        await cursor.execute(f"SELECT info FROM langinfo WHERE guild_id = {message.guild.id}")
        langinfo = await cursor.fetchone()
        if str(langinfo) != "None" :
            langinfo = langinfo[0]

        if result is not None : # Si un channel est lié à un autre channel
            
            if type(message.channel) is Thread :
                await cursor.close()
                return
            
            result[0], result[1] = int(result[0]), int(result[1])
            if channel_id == int(result[0]) : # Si le channel actuel est le channel 1
                SOURCE_LANG = self.bot.LANGCODES[result[2]]
                DESTINATION_LANG = self.bot.LANGCODES[result[3]]
                DESTINATION_CHANNEL = result[1]
                DESTINATION_WEBHOOK = result[5]
            else : # Si le channel actuel est le channel 2
                SOURCE_LANG = self.bot.LANGCODES[result[3]]
                DESTINATION_LANG = self.bot.LANGCODES[result[2]]
                DESTINATION_CHANNEL = result[0]
                DESTINATION_WEBHOOK = result[4]
            
            # On traduit le message dans la 1ère langue
            try :
                temp_lo = await self.bot.trad.detect(message.content)
                langue_originale = temp_lo.lang
            except :
                temp_lo = await self.bot.trad.detect_legacy(message.content)
                langue_originale = temp_lo.lang
            
            if result[4] is None :
                try :
                    chan = await self.bot.fetch_channel(result[0])
                except errors.NotFound :
                    await cursor.execute(f"DELETE FROM linkchannels WHERE guild_id = {message.guild.id} AND channel_id_1 = {result[0]}")
                    await self.bot.db.commit()
                    await cursor.close()
                    return
                try:
                    webhook = await chan.create_webhook(name="Translator Bot")
                except :
                    await message.reply(f"I am missing the `Manage Webhooks` permission in the <#{result[0]}> channel.\nPlease give me the permission globally or for the channel only if you are an admin and try again.\nIf you are not an admin, please ask an admin to give me the permission.")
                    await cursor.close()
                    return
                sql = f"UPDATE linkchannels SET webhook_1 = ? WHERE guild_id = ? AND channel_id_1 = ?"
                val = (webhook.url, message.guild.id, result[0])
                await cursor.execute(sql,val)
                await self.bot.db.commit()

                result[4] = webhook.url
            
            if result[5] is None :
                try :
                    chan = await self.bot.fetch_channel(result[1])
                except errors.NotFound :
                    await cursor.execute(f"DELETE FROM linkchannels WHERE guild_id = {message.guild.id} AND channel_id_1 = {result[1]}")
                    await self.bot.db.commit()
                    await cursor.close()
                    return
                try :
                    webhook = await chan.create_webhook(name="Translator Bot")
                except :
                    await message.reply(f"I am missing the `Manage Webhooks` permission in the <#{result[1]}> channel.\nPlease give me the permission globally or for the channel only if you are an admin and try again.\nIf you are not an admin, please ask an admin to give me the permission.")
                    await cursor.close()
                    return
                sql = f"UPDATE linkchannels SET webhook_2 = ? WHERE guild_id = ? AND channel_id_2 = ?"
                val = (webhook.url, message.guild.id, result[1])
                await cursor.execute(sql,val)
                await self.bot.db.commit()

                result[5] = webhook.url

            if (langue_originale == SOURCE_LANG) or (len(message.content) == 0 and len(message.attachments) > 0) :

                if DESTINATION_WEBHOOK is None :
                    if DESTINATION_CHANNEL == result[0] :
                        DESTINATION_WEBHOOK = result[4]
                    else :
                        DESTINATION_WEBHOOK = result[5]
                
                try: # On tente de traduire le message
                    Traduction = await self.bot.trad.translate(text = message.content, dest=DESTINATION_LANG)
                except :
                    try:
                        Traduction = await self.bot.trad.translate_to_detect(text = message.content, dest=DESTINATION_LANG)
                    except :
                        await cursor.close()
                        return

                if Traduction.src == 'auto' :
                    Traduction.src = langue_originale
                
                Traduction.text = await self.is_custom_emoji(message.content, Traduction.text)

                is_same_message_content = await self.bot.loop.run_in_executor(None, self.compare_messages, message.content, Traduction.text)
                is_same_message_only = await self.bot.loop.run_in_executor(None, self.compare_messages, MessageOnly, Traduction.text)
                if is_same_message_content or is_same_message_only :
                    Traduction.text = message.content
                
                if (langinfo == "enabled") and (True not in [is_same_message_content, is_same_message_only]) :
                    flag = self.bot.LANGUAGES[Traduction.src]
                    Traduction.text = f"`{flag}` {Traduction.text}"
                
                if is_url :
                    Traduction.text = message.content
                
                async with aiohttp.ClientSession() as session:

                    try :
                        webhook = Webhook.from_url(DESTINATION_WEBHOOK, session=session)
                        await webhook.fetch()
                    except :
                        try :
                            chan = await self.bot.fetch_channel(DESTINATION_CHANNEL)
                        except errors.NotFound :
                            await cursor.execute(f"DELETE FROM linkchannels WHERE guild_id = {message.guild.id} AND channel_id_1 = {DESTINATION_CHANNEL}")
                            await self.bot.db.commit()
                            await cursor.close()
                            return
                        webhook = await chan.create_webhook(name="Translator Bot")
                        if DESTINATION_CHANNEL == result[0] :
                            sql = f"UPDATE linkchannels SET webhook_1 = ? WHERE guild_id = ? AND channel_id_1 = ?"
                            val = (webhook.url, message.guild.id, result[0])
                        else :
                            sql = f"UPDATE linkchannels SET webhook_2 = ? WHERE guild_id = ? AND channel_id_2 = ?"
                            val = (webhook.url, message.guild.id, result[1])
                        await cursor.execute(sql,val)
                        await self.bot.db.commit()

                    if len(Traduction.text) > 2000:
                        parts = await self.split_message_into_parts(Traduction.text)
                        if len(message.attachments) > 0:
                            attachments = []
                            for attachment in message.attachments :
                                attachment = await attachment.to_file()
                                attachments.append(attachment)
                        for x in range(len(parts)):
                            if (x == len(parts) - 1) and (len(message.attachments) > 0):
                                await webhook.send(content=parts[x], username=message.author.display_name, avatar_url=message.author.avatar.url if message.author.avatar is not None else None, files=attachments)
                            else :
                                await webhook.send(content=parts[x], username=message.author.display_name, avatar_url=message.author.avatar.url if message.author.avatar is not None else None)
                    
                    elif len(Traduction.text) == 0 and len(message.attachments) == 0:
                        messagecontent = f"{message.jump_url}\nCould not translate this message. If you think this is an error, please contact UnBonWhisky on github or unbonwhisky on discord.\nOriginal message:\n{message.content}"
                        if len(messagecontent) > 2000:
                            await self.split_message_into_parts(messagecontent)
                            for x in range(len(parts)):
                                await webhook.send(content=parts[x], username=message.author.display_name, avatar_url=message.author.avatar.url if message.author.avatar is not None else None)
                        else :
                            await webhook.send(content=messagecontent, username=message.author.display_name, avatar_url=message.author.avatar.url if message.author.avatar is not None else None)
                    
                    elif len(Traduction.text) == 0 and len(message.attachments) > 0:
                        attachments = []
                        for attachment in message.attachments :
                            attachment = await attachment.to_file()
                            attachments.append(attachment)
                        await webhook.send(username=message.author.display_name, avatar_url=message.author.avatar.url if message.author.avatar is not None else None, files=attachments)
                    
                    else :
                        if len(message.attachments) > 0:
                            attachments = []
                            for attachment in message.attachments :
                                attachment = await attachment.to_file()
                                attachments.append(attachment)
                            await webhook.send(content=Traduction.text, username=message.author.display_name, avatar_url=message.author.avatar.url if message.author.avatar is not None else None, files=attachments)
                        else :
                            await webhook.send(content=Traduction.text, username=message.author.display_name, avatar_url=message.author.avatar.url if message.author.avatar is not None else None)
                await cursor.close()
                return

        if is_url:
            await cursor.close()
            return
        
        # On vérifie si un reversed est activé pour ce channel
        await cursor.execute(f"SELECT language_1, language_2 FROM reversed WHERE guild_id = {message.guild.id} AND channel_id = {channel_id}")
        result = await cursor.fetchone()
        if result is not None :
            result = list(result)
            if result[0] is None :
                result = None

        DESTINATION = None

        if result is not None : # Si un reversed est activé pour ce channel

            # On récupère les langues du reversed
            language_1 = self.bot.LANGCODES[result[0]]
            language_2 = self.bot.LANGCODES[result[1]]

            # On traduit le message dans la 1ère langue
            try :
                temp_lo = await self.bot.trad.detect(message.content)
                langue_originale = temp_lo.lang
            except :
                temp_lo = await self.bot.trad.detect_legacy(message.content)
                langue_originale = temp_lo.lang

            if langue_originale in [language_1, language_2] :
                
                if langue_originale == language_1 :
                    DESTINATION=language_2
                else :
                    DESTINATION=language_1
        
        if DESTINATION is None :
            # On récupère la langue du channel
            await cursor.execute(f"SELECT language FROM channel_language WHERE guild_id = {message.guild.id} AND channel_id = {channel_id}")
            result = await cursor.fetchone()

            if result is not None : # Si la langue du channel a été définie par un admin du serveur
                source = self.bot.LANGCODES[result[0]]

                if source == "none": # Si la langue du channel est "none", on ne fait rien
                    await cursor.close()
                    return
                else: 
                    DESTINATION = source
            
        if DESTINATION is None :
            # On récupère la langue du serveur
            await cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {message.guild.id}")
            result = await cursor.fetchone()

            if (result is not None) and (result[0] is not None) : # Si la langue du serveur a été définie par un admin du serveur
                source = self.bot.LANGCODES[result[0]]

                if source == "none": # Si la langue du serveur est "none", on ne fait rien
                    await cursor.close()
                    return
                else:
                    DESTINATION = source

        if DESTINATION is not None :
            # On traduit le message
            try :
                Traduction = await self.bot.trad.translate(text = message.content, dest=DESTINATION)
            except :
                try :
                    Traduction = await self.bot.trad.translate_to_detect(text = message.content, dest=DESTINATION)
                except :
                    await cursor.close()
                    return
            
            if Traduction.src == 'auto' :
                try :
                    temp_lo = await self.bot.trad.detect(message.content)
                    Traduction.src = temp_lo.lang
                except :
                    temp_lo = await self.bot.trad.detect_legacy(message.content)
                    Traduction.src = temp_lo.lang

            is_same_message_content = await self.bot.loop.run_in_executor(None, self.compare_messages, message.content, Traduction.text)
            is_same_message_only = await self.bot.loop.run_in_executor(None, self.compare_messages, MessageOnly, Traduction.text)
            
            if Traduction.src == DESTINATION : # Si la langue source est la même que la langue de traduction, on ne fait rien
                await cursor.close()
                return
            elif message.content == Traduction.text : # Si le contenu du message est le même que la traduction, on ne fait rien
                await cursor.close()
                return
            elif Traduction.text == "" : # Si la traduction est vide, on ne fait rien
                await cursor.close()
                return
            elif is_same_message_content or is_same_message_only : # Si le message traduit a une séquence trop ressemblante au message original, on ne fait rien
                await cursor.close()
                return
            else :
                Traduction.text = await self.is_custom_emoji(message.content, Traduction.text)
                
                if langinfo == "enabled" :
                    flag = self.bot.LANGUAGES[Traduction.src]
                    Traduction.text = f"`{flag}` {Traduction.text}"
                
                try: # On tente de répondre au message
                    if len(Traduction.text) > 2000:
                        parts = await self.split_message_into_parts(Traduction.text)
                        for x in range(len(parts)):
                            if x == 0:
                                await message.reply(content=parts[x], mention_author=False)
                                await cursor.close()
                                return
                            else:
                                await message.channel.send(content=parts[x])
                                await cursor.close()
                                return
                    elif len(Traduction.text) == 0:
                        await cursor.close()
                        return
                    else :
                        await message.reply(content=Traduction.text, mention_author=False)
                        await cursor.close()
                        return
                except :
                    await cursor.close()
                    return
    

def setup(bot):
    print("Message Translator is ready !")
    bot.add_cog(MessageTranslator(bot))
