from discord import Embed, ApplicationContext, default_permissions, InteractionContextType
from discord.ext.commands import slash_command, Cog
from discord.ext import pages

class FAQCommand(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.pages = []
        for i in range(8):
            self.pages.append(Embed(
                title = "FAQ",
                description = "Frequently Asked Questions",
                color = 0x5865F2,
                url="https://github.com/UnBonWhisky/Translator-Bot/blob/main/FAQ.md"
            ))
        
        self.pages[0].add_field(
            name="How do I set up auto translations on the bot ?",
            value=f"you have got 3 ways :\n- `/defaultlanguage` : that set up auto translation on all channels for 1 language\n- `/channellanguage` : that set up auto translation on 1 channel for 1 language\n- `/reverse` : that set up auto translation from lang1 to lang2, and lang2 to lang1\n    - if a message is sent using a lang3, then it will use the `/channellanguage` or `/defaultlanguage` configuration\n- `/linkchannels` : that set up auto translation from lang1 in chan1 and lang2 in chan2. All messages sent in lang1 in chan1 will be translated and sent in the lang2 in chan2\n    - if a message is sent in another language, it will correspond to the first occurence in the priority order shown below\n\nThe priority order of the bot is the following one :\n1. `/linkchannels`\n2. `/reverse`\n3. `/channellanguage`\n4. `/defaultlanguage`\n\n:warning: If you have set up the `/reverse` and `/linkchannels` with the same language, the `/reverse` will work in only one way, like a `/channellanguage` because of the priority",
            inline=False
        )
        self.pages[1].add_field(
            name="I tried to set up auto translation but the bot does not respond to the messages. Why ?",
            value="If the bot does not respond to your messages, it is surely a permission issue with your server / channel.\nJust give it an admin role or the admin permissions to see if this is the problem. If it is, you can now troubleshoot to understand why it does not work without.\nBy default, the bot permissions are the right ones (if you are inviting it from the Discord App Directory).\n:warning: With link channels, the bot needs the `Manage Webhooks` permissions, which have been added to the default perms with the update of the bot",
            inline=False
        )
        self.pages[2].add_field(
            name="Is it possible to translate to more than one language ?",
            value="Actually no, there is no such feature on the bot, this is because of the API I use.",
            inline=False
        )
        self.pages[3].add_field(
            name="Is there a way each user see it own translation of a message ?",
            value="No. Discord only allow ephemeral messages to be sent when using a slash command. So there is no way to build this feature actually.",
            inline=False
        )
        self.pages[4].add_field(
            name="How do I translate some messages but not automatically ?",
            value="If you are receiving the message, you can just use the flag reactions, it will translate the message depending of the flag used.\nExample :\n- :flag_fr: = translation to french\n- :flag_us: = translation to english\nIf you are sending a message and want to send it already translated, you can use the `/translate` command.\nAs of <t:1724484660:d>, you can now use the \"Apps\" context menu to get a translation into your language. This one works in DM's too.\nThe `/personal` command let you change the output language for the **Translate** Apps command.",
            inline=False
        )
        self.pages[5].add_field(
            name="How do I remove the 4 embeds that are printed when I am using flag reactions ?",
            value="The `/allowflag` command provide some options you can use to edit the comportment of the bot like sending minimalist messages or to set a timeout on after a flag reaction message.",
            inline=False
        )
        self.pages[6].add_field(
            name="Is it possible to have the translation of a message but in another channel ?",
            value="Sure you can ! As of <t:1723034640:d>, the `/linkchannels` command have been added to the bot",
            inline=False
        )
        self.pages[7].add_field(
            name="Is it possible to have more than 2 `/linkchannels` ?",
            value="Actually no, because of the API I am using and for stability for all the users, I do not provide this configuration.\nI limit the bot so that it only uses a message in one language as input, and a message in another language as output. No more.\nIt is a highly requested feature that can be implemented in the future, but I can not provide any ETA about it.",
            inline=False
        )
    
    async def get_pages(self):
        return self.pages
        
    @slash_command(
        name ="faq",
        description = "Get the FAQ of the bot.",
        contexts={InteractionContextType.guild}
    )
    @default_permissions(administrator=True)
    async def faq(self, ctx : ApplicationContext):
            
        await ctx.defer(ephemeral=True)
        
        paginator = pages.Paginator(pages=await self.get_pages())
        
        await paginator.respond(ctx.interaction, ephemeral=True)

def setup(bot):
    print("FAQ Command cog ready !")
    bot.add_cog(FAQCommand(bot))