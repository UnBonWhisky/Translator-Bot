from discord import Embed, ApplicationContext, InteractionContextType
from discord.ext.commands import slash_command, Cog
from discord.ext import pages

class Help(Cog):
    def __init__(self, bot) :
        self.bot = bot

        # Déclaration des pages de base :
        self.pages = [
            Embed(
                title="Commands for everyone",
                description="Here are the commands that everyone can use.",
                color=0x5865F2
            ),
            Embed(
                title="Commands for administrators",
                description="Here are the commands that only administrators can use.",
                color=0x5865F2
            )
        ]

        # Déclaration des footers et des auteurs des pages :
        for page in self.pages :
            page.set_footer(
                icon_url = f"https://cdn.discordapp.com/avatars/341257685901246466/ee4062cd8d5888421a51c2fc9875b9df.png?size=4096",
                text = f"unbonwhisky"
            )
            try :
                page.set_author(
                    name = self.bot.user.display_name,
                    icon_url = self.bot.user.avatar.url
                )
            except :
                pass
        
        # Déclaration des fields de la page 1 :
        self.pages[0].add_field(
            name="/help",
            value="To show all available commands. It is this command.",
            inline=True
        )
        self.pages[0].add_field(
            name="/stats",
            value="Show all stats of my bot.",
            inline=True
        )
        self.pages[0].add_field(
            name="/translate",
            value="Use this command to translate a text in a specific language.\n**This command is user installable.**",
            inline=False
        )
        self.pages[0].add_field(
            name="/translatechoice",
            value="Use this command if you want to have the flag reactions translations in DM or in the channel of the message.",
            inline=False
        )
        self.pages[0].add_field(
            name="/donation",
            value="Show all infos you need to know to how to make me a donation. Prices are on the websites.",
            inline=False
        )

        # Déclaration des fields de la page 2 :
        self.pages[1].add_field(
            name="/languagelist",
            value="To show all languages the bot support.\nType this command to have the full languages list.",
            inline=False
        )
        self.pages[1].add_field(
            name="/linkchannels",
            value="To set a translation between two languages in two different channels.",
            inline=False
        )
        self.pages[1].add_field(
            name="/reverse",
            value="To set a reversed translation between two languages in the same channel.",
            inline=False
        )
        self.pages[1].add_field(
            name="/channellanguage",
            value="To set a different language as your default language in a specific channel.\n`none` can be used to disable translations in a specific channel.",
            inline=False
        )
        self.pages[1].add_field(
            name="/defaultlanguage",
            value="To set a default language to translate all messages of the servers that are not in this language.",
            inline=False
        )
        self.pages[1].add_field(
            name="/allowflag",
            value="To manage the flag reaction translation.\nThis command allows you to force the `/translatechoice` command and some other things.",
            inline=False
        )
        self.pages[1].add_field(
            name="/resetsettings",
            value="To reset all your settings.\nType this command to have more infos about it.",
            inline=False
        )
        self.pages[1].add_field(
            name="/support",
            value="To send a support message to the bot owner from the bot.\nCheck your DM's in case of the bot owner answer you or add you as friend (unbonwhisky / JeSuisUnBonWhisky).",
            inline=True
        )
        self.pages[1].add_field(
            name="Support server",
            value="Join the support server if you need help by [clicking here](https://discord.gg/gqfFqJp)",
            inline=True
        )

    async def get_pages(self, number = None):
        if number:
            return self.pages[number]
        else:
            return self.pages


    @slash_command(
        name="help",
        description="Display the help message.",
        contexts={InteractionContextType.guild}
    )
    async def help(self, ctx: ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        if ctx.author.guild_permissions.administrator:
            HelpPage = await self.get_pages()
            paginator = pages.Paginator(pages=HelpPage)
        else :
            HelpPage = await self.get_pages(number=0)
            paginator = pages.Paginator(pages=HelpPage)
        
        paginator.remove_button("first")
        paginator.remove_button("last")
        
        await paginator.respond(ctx.interaction, ephemeral=True)



def setup(bot):
    print("Help command is ready !")
    bot.add_cog(Help(bot))
