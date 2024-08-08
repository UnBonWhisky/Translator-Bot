from discord import Embed, ApplicationContext
from discord.ext.commands import slash_command, Cog

class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="help",
        description="Display the help message.",
        guild_only=True
    )
    async def help(self, ctx: ApplicationContext):
        
        await ctx.defer(ephemeral=True)
        
        embed = Embed(
            title="Available commands :",
            color=0x5865F2
        )
        # Footer :
        embed.set_footer(
            icon_url = f"https://cdn.discordapp.com/avatars/341257685901246466/ee4062cd8d5888421a51c2fc9875b9df.png?size=4096",
            text = f"unbonwhisky"
        )
        # Author :
        embed.set_author(
            name = self.bot.user.display_name,
            icon_url= self.bot.user.avatar.url
        )
        # Fields :
        embed.add_field(
            name="/help",
            value="To show all available commands. It is this command.",
            inline=True
        )
        embed.add_field(
            name="/stats",
            value="Show all stats of my bot.",
            inline=True
        )
        embed.add_field(
            name="/invite",
            value="Show all links that may be useful (for you and for me).",
            inline=True
        )
        embed.add_field(
            name="/translatechoice",
            value="Use this command if you want to have the flag reactions translations in DM or in the channel of the message.",
            inline=False
        )
        embed.add_field(
            name="/donation",
            value="Show all infos you need to know to how to make me a donation. Prices are on the websites.",
            inline=False
        )
        if ctx.author.guild_permissions.administrator:
            embed.add_field(
                name="/languagelist",
                value="To show all languages the bot support.\nType this command to have the full languages list.",
                inline=False
            )
            embed.add_field(
                name="/reverse",
                value="To set a reversed translation between two languages in the same channel.",
                inline=False
            )
            embed.add_field(
                name="/channellanguage",
                value="To set a different language as your default language in a specific channel.",
                inline=False
            )
            embed.add_field(
                name="/defaultlanguage",
                value="To set a default language to translate all messages of the servers that are not in this language.",
                inline=False
            )
            embed.add_field(
                name="/resetsettings",
                value="To reset all your settings.\nType this command to have more infos about it.",
                inline=False
            )
            embed.add_field(
                name="/allowflag",
                value="To enabled or disable the flag reaction translation.",
                inline=False
            )
            embed.add_field(
                name="/support",
                value="To send a support message to the bot owner from the bot.\nCheck your DM's in case of the bot owner answer you.",
                inline=True
            )
            embed.add_field(
                name="Support server",
                value="Join the support server if you need help by [clicking here](https://discord.gg/gqfFqJp)",
                inline=True
            )

        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    print("Help command is ready !")
    bot.add_cog(Help(bot))
