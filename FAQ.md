# FAQ - Translator Bot

Here you will find some informations about how `Translator Bot` works, and answers to the most frequently asked questions.

## How do I set up auto translations on the bot ?

you have got 3 ways :  
- `/defaultlanguage` : that set up auto translation on all channels for 1 language
- `/channellanguage` : that set up auto translation on 1 channel for 1 language
- `/reverse` : that set up auto translation from lang1 to lang2, and lang2 to lang1
    - if a message is sent using a lang3, then it will use the `/channellanguage` or `/defaultlanguage` configuration
- `/linkchannels` : that set up auto translation from lang1 in chan1 and lang2 in chan2. All messages sent in lang1 in chan1 will be translated and sent in the lang2 in chan2
    - if a message is sent in another language, it will correspond to the first occurence in the priority order shown below

The priority order of the bot is the following one :
1. `/linkchannels`
2. `/reverse`
3. `/channellanguage`
4. `/defaultlanguage`

:warning: If you have set up the `/reverse` and `/linkchannels` with the same language, the `/reverse` will work in only one way, like a `/channellanguage` because of the priority

## I tried to set up auto translation but the bot does not respond to the messages. Why ?

If the bot does not respond to your messages, it is surely a permission issue with your server / channel.  

Just give it an admin role or the admin permissions to see if this is the problem. If it is, you can now troubleshoot to understand why it does not work without.

By default, the bot permissions are the right ones (if you are inviting it from the Discord App Directory).

:warning: With link channels, the bot needs the `Manage Webhooks` permissions, which have been added to the default perms with the update of the bot

## Is it possible to translate to more than one language ?

Actually no, there is no such feature on the bot, this is because of the API I use.

## Is there a way each user see it own translation of a message ?

No. Discord only allow ephemeral messages to be sent when using a slash command. So there is no way to build this feature actually.

## How do I translate some messages but not automatically ?

If you are receiving the message, you can just use the flag reactions, it will translate the message depending of the flag used.  
Example :  
- :flag_fr: = translation to french  
- :flag_us: = translation to english

If you are sending a message and want to send it already translated, you can use the `/translate` command.

## How do I remove the 4 embeds that are printed when I am using flag reactions ?

The `/allowflag` command provide some options you can use to edit the comportment of the bot like sending minimalist messages or to set a timeout on after a flag reaction message.

## Is it possible to have the translation of a message but in another channel ?

~~Actually no. I will work on this feature but it is not actually available on the bot.~~  
Sure you can ! As of August 7th 2024, the `/linkchannels` command have been added to the bot