from discord import Thread
from discord.ext.commands import Cog

import aiosqlite, re
from googletrans import Translator
from difflib import SequenceMatcher

# Connexion au service de traduction google translate

class MessageTranslator(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactionflag = ['🇦🇸','🇦🇨','🇦🇩','🇦🇪','🇦🇬','🇦🇮','🇦🇱','🇦🇲','🇦🇴','🇦🇶','🇦🇷','🇦🇹','🇦🇺','🇦🇼','🇦🇽','🇦🇿','🇧🇸','🇧🇦','🇧🇧','🇧🇩','🇧🇪','🇧🇫','🇧🇬','🇧🇭','🇧🇮','🇧🇯','🇧🇱','🇧🇲','🇧🇳','🇧🇴','🇧🇶','🇧🇷','🇧🇹','🇧🇻','🇧🇼','🇧🇾','🇧🇿','🇨🇦','🇨🇨','🇨🇩','🇨🇫','🇨🇬','🇨🇭','🇨🇮','🇨🇰','🇨🇱','🇨🇲','🇨🇳','🇨🇴','🇨🇵','🇨🇷','🇨🇺','🇨🇻','🇨🇼','🇨🇽','🇨🇾','🇨🇿','🇩🇪','🇩🇬','🇩🇯','🇩🇰','🇩🇲','🇩🇴','🇩🇿','🇪🇦','🇪🇨','🇪🇪','🇪🇬','🇪🇭','🇪🇷','🇪🇸','🇪🇹','🇪🇺','🇫🇮','🇫🇯','🇫🇰','🇫🇲','🇫🇴','🇫🇷','🇬🇦','🇬🇧','🇬🇩',' 🇬🇪','🇬🇫','🇬🇬','🇬🇭','🇬🇮','🇬🇱','🇬🇲','🇬🇳','🇬🇵','🇬🇶','🇬🇷','🇬🇸','🇬🇹','🇬🇺','🇬🇼','🇬🇾','🇭🇰',' 🇭🇲','🇭🇳','🇭🇷','🇭🇹','🇭🇺','🇮🇨','🇮🇩','🇮🇪','🇮🇱','🇮🇲','🇮🇳','🇮🇴','🇮🇶','🇮🇷','🇮🇸','🇮🇹','🇯🇪',' 🇯🇲','🇯🇴','🇯🇵','🇰🇪','🇰🇬','🇰🇭','🇰🇮','🇰🇲','🇰🇳','🇰🇵','🇰🇷','🇰🇼','🇰🇾','🇰🇿','🇱🇦','🇱🇧','🇱🇨',' 🇱🇮','🇱🇰','🇱🇷','🇱🇸','🇱🇹','🇱🇺','🇱🇻','🇱🇾','🇲🇦','🇲🇨','🇲🇩','🇲🇪','🇲🇫','🇲🇬','🇲🇭','🇲🇰','🇲🇱',' 🇲🇲','🇲🇳','🇲🇴','🇲🇵','🇲🇶','🇲🇷','🇲🇸','🇲🇹','🇲🇺','🇲🇻','🇲🇼','🇲🇽','🇲🇾','🇲🇿','🇳🇦','🇳🇨','🇳🇪',' 🇳🇫','🇳🇬','🇳🇮','🇳🇱','🇳🇴','🇳🇵','🇳🇷','🇳🇺','🇳🇿','🇴🇲','🇵🇦','🇵🇪','🇵🇫','🇵🇬','🇵🇭','🇵🇰','🇵🇱',' 🇵🇲','🇵🇳','🇵🇷','🇵🇸','🇵🇹','🇵🇼','🇵🇾','🇶🇦','🇷🇪','🇷🇴','🇷🇸','🇷🇺','🇷🇼','🇸🇦','🇸🇧','🇸🇨','🇸🇩',' 🇸🇪','🇸🇬','🇸🇭','🇸🇮','🇸🇯','🇸🇰','🇸🇱','🇸🇲','🇸🇳','🇸🇴','🇸🇷','🇸🇸','🇸🇹','🇸🇻','🇸🇽','🇸🇾','🇸🇿',' 🇹🇦','🇹🇨','🇹🇩','🇹🇫','🇹🇬','🇹🇭','🇹🇯','🇹🇰','🇹🇱','🇹🇲','🇹🇳','🇹🇴','🇹🇷','🇹🇹','🇹🇻','🇹🇼','🇹🇿',' 🇺🇦','🇺🇬','🇺🇲','🇺🇳','🇺🇸','🇺🇾','🇺🇿','🇻🇦','🇻🇨','🇻🇪','🇻🇬','🇻🇮','🇻🇳','🇻🇺','🇼🇫','🇼🇸','🇽🇰',' 🇾🇪','🇾🇹','🇿🇦','🇿🇲','🇿🇼','🇺🇦','🇸🇪','🏴󠁧󠁢󠁥󠁮󠁧󠁿','🏴󠁧󠁢󠁷󠁬󠁳󠁿']
        self.destinationflag = ['sm','en','ca','ar','en','en','sq','hy','pt','en','es','de','en','nl','sv','az','en','bs','en','bn','fr','fr','bg','ar','fr','fr','fr','en','ms','es','nl','pt','ne','is','en','be','en','en','en','fr','fr','fr','de','fr','mi','es','fr','zh-cn','es','fr','es','es','pt','nl','zh-cn','el','cs','de','en','fr','da','en','es','ar','es','es','et','ar','ar','en','es','am','en','fi','hi','en','en','da','fr','fr','en','en','ka','fr','en','en','en','en','en','fr','fr','fr','el','en','es','en','pt','en','zh-cn','en','es','hr','ht','hu','es','id','ga','iw','en','hi','en','ku','fa','is','it','en','en','ar','ja','sw','ky','km','en','fr','en','ko','ko','ar','en','kk','lo','ar','en','ge','ta','en','en','lt','lb','lv','ar','ar','fr','ro','en','fr','mg','en','mk','fr','my','mn','zh-cn','en','fr','ar','en','mt','en','en','en','es','ms','pt','en','fr','fr','en','en','es','nl','no','ne','en','en','mi','ar','es','es','fr','en','tl','en','pl','fr','en','es','ar','pt','en','es','ar','fr','ro','sr','ru','en','ar','en','fr','ar','sv','ms','en','sl','nl','sk','en','it','fr','so','nl','en','pt','es','nl','ar','en','en','en','fr','fr','fr','th','tg','en','pt','en','ar','en','tr','en','en','zh-cn','sw','uk','sw','en','en','en','es','uz','it','en','es','en','en','vi','fr','fr','sm','sq','ar','fr','af','en','sn','uk','sv','en','cy']
        
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
    
    async def compare_messages(self, original_message, translated_message):
        original_normalized = re.sub(r'\s+', '', original_message).lower()
        translated_normalized = re.sub(r'\s+', '', translated_message).lower()
        
        if original_normalized == translated_normalized:
            return True
        
        # Utiliser SequenceMatcher pour évaluer la similarité entre les chaînes
        ratio = SequenceMatcher(None, original_normalized, translated_normalized).ratio()
        return ratio >= 0.75

    @Cog.listener()
    async def on_message(self, message):
        
        is_url = await self.is_url(message.content)
        is_emoji_or_mention = await self.is_emoji_or_mention(message.content)

        # Si l'auteur du message est un bot ou le message vient d'un MP, on ne fait rien
        if (message.author.bot is True) or (message.guild is None) or (message.content == '') or (is_emoji_or_mention) :
            return

        # On retire les caractères spéciaux du message pour un test de traduction basé sur la séquence
        MessageOnly = ''.join(item for item in message.content if item.isalnum())

        LANGUAGES = [None, 'None', 'none','afrikaans','albanian','amharic','arabic','armenian','azerbaijani','basque','belarusian','bengali','bosnian','bulgarian','catalan','cebuano','chichewa','chinese (simplified)','chinese (traditional)','corsican','croatian','czech','danish','dutch','english','esperanto','estonian','filipino','finnish','french','frisian','galician','georgian','german','greek','gujarati','haitian creole','hausa','hawaiian','hebrew','hebrew','hindi','hmong','hungarian','icelandic','igbo','indonesian','irish','italian','japanese','javanese','kannada','kazakh','khmer','korean','kurdish (kurmanji)','kyrgyz','lao','latin','latvian','lithuanian','luxembourgish','macedonian','malagasy','malay','malayalam','maltese','maori','marathi','mongolian','myanmar (burmese)','nepali','norwegian','odia','pashto','persian','polish','portuguese','punjabi','romanian','russian','samoan','scots gaelic','serbian','sesotho','shona','sindhi','sinhala','slovak','slovenian','somali','spanish','sundanese','swahili','swedish','tajik','tamil','telugu','thai','turkish','ukrainian','urdu','uyghur','uzbek','vietnamese','welsh','xhosa','yiddish','yoruba','zulu']

        LANGUAGESEXT = ['none', 'none', 'none','af','sq','am','ar','hy','az','eu','be','bn','bs','bg','ca','ceb','ny','zh-cn','zh-tw','co','hr','cs','da','nl','en','eo','et','tl','fi','fr','fy','gl','ka','de','el','gu','ht','ha','haw','iw','he','hi','hmn','hu','is','ig','id','ga','it','ja','jw','kn','kk','km','ko','ku','ky','lo','la','lv','lt','lb','mk','mg','ms','ml','mt','mi','mr','mn','my','ne','no','or','ps','fa','pl','pt','pa','ro','ru','sm','gd','sr','st','sn','sd','si','sk','sl','so','es','su','sw','sv','tg','ta','te','th','tr','uk','ur','ug','uz','vi','cy','xh','yi','yo','zu']

        if type(message.channel) is Thread: # Si le message est envoyé dans un thread, on récupère le channel de base
            channel_id = message.channel.parent_id
        else : # Sinon, on récupère le channel actuel
            channel_id = message.channel.id

        cursor = await self.bot.db.cursor()

        await cursor.execute(f"SELECT channel_id_1, channel_id_2, language_1, language_2 FROM linkchannels WHERE guild_id = {message.guild.id} AND (channel_id_1 = {channel_id} OR channel_id_2 = {channel_id})")
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
                SOURCE_LANG = LANGUAGESEXT[LANGUAGES.index(result[2])]
                DESTINATION_LANG = LANGUAGESEXT[LANGUAGES.index(result[3])]
                DESTINATION_CHANNEL = result[1]
            else : # Si le channel actuel est le channel 2
                SOURCE_LANG = LANGUAGESEXT[LANGUAGES.index(result[3])]
                DESTINATION_LANG = LANGUAGESEXT[LANGUAGES.index(result[2])]
                DESTINATION_CHANNEL = result[0]
            
            # On traduit le message dans la 1ère langue
            try :
                temp_lo = await self.bot.trad.detect(message.content)
                langue_originale = temp_lo.lang.lower()
            except :
                temp_lo = await self.bot.trad.detect_legacy(message.content)
                langue_originale = temp_lo.lang.lower()
            
            if langue_originale == SOURCE_LANG :
                dest_chan = await self.bot.fetch_channel(DESTINATION_CHANNEL)
                try: # On tente de récupérer les webhooks du channel de destination
                    webhooks = await dest_chan.webhooks()
                    if webhooks == []:
                        webhook = await dest_chan.create_webhook(name="Translator Bot")
                    else :
                        webhook = webhooks[0]
                except:
                    await message.reply(f"I am missing the `Manage Webhooks` permission in the <#{DESTINATION_CHANNEL}> channel.\nPlease give me the permission globally or for the channel only if you are an admin and try again.\nIf you are not an admin, please ask an admin to give me the permission.")
                    await cursor.close()
                    return
                
                try: # On tente de traduire le message
                    Traduction = await self.bot.trad.translate(text = message.content, dest=DESTINATION_LANG)
                except:
                    try:
                        Traduction = await self.bot.trad.translate_to_detect(text = message.content, dest=DESTINATION_LANG)
                    except:
                        await cursor.close()
                        return
                
                if Traduction.src == 'auto' :
                    Traduction.src = langue_originale
                
                Traduction.text = await self.is_custom_emoji(message.content, Traduction.text)

                is_same_message_content = await self.compare_messages(message.content, Traduction.text)
                is_same_message_only = await self.compare_messages(MessageOnly, Traduction.text)
                if is_same_message_content or is_same_message_only :
                    Traduction.text = message.content
                
                if (langinfo == "enabled") and (True not in [is_same_message_content, is_same_message_only]) :
                    flag = LANGUAGES[LANGUAGESEXT.index(Traduction.src)]
                    Traduction.text = f"`{flag.lower()}` {Traduction.text}"
                
                if is_url :
                    Traduction.text = message.content
                
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
            language_1 = LANGUAGESEXT[LANGUAGES.index(result[0])]
            language_2 = LANGUAGESEXT[LANGUAGES.index(result[1])]

            # On traduit le message dans la 1ère langue
            try :
                temp_lo = await self.bot.trad.detect(message.content)
                langue_originale = temp_lo.lang.lower()
            except :
                temp_lo = await self.bot.trad.detect_legacy(message.content)
                langue_originale = temp_lo.lang.lower()

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
                source = LANGUAGESEXT[LANGUAGES.index(result[0])]

                if source == "none": # Si la langue du channel est "none", on ne fait rien
                    await cursor.close()
                    return
                else: 
                    DESTINATION = source
            
        if DESTINATION is None :
            # On récupère la langue du serveur
            await cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {message.guild.id}")
            result = await cursor.fetchone()

            if result is not None : # Si la langue du serveur a été définie par un admin du serveur
                source = LANGUAGESEXT[LANGUAGES.index(result[0])]

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

            is_same_message_content = await self.compare_messages(message.content, Traduction.text)
            is_same_message_only = await self.compare_messages(MessageOnly, Traduction.text)
            
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
                    flag = LANGUAGES[LANGUAGESEXT.index(Traduction.src.lower())]
                    Traduction.text = f"`{flag.lower()}` {Traduction.text}"
                
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
