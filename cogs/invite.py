from discord import Embed, ApplicationContext
from discord.ext.commands import slash_command, Cog

class InviteCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "invite",
        description = "Anything you need to know if you want me on your server",
        guild_only=True
    )
    async def invite(self, ctx : ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        embed = Embed(title="Join author's server here",
                              url='https://discord.gg/gqfFqJp',
                              description="For management, ideas I can code and others things to have a better bot",
                              color = 0x5865F2
                              )
        # Author :
        embed.set_author(
            name = self.bot.user.display_name,
            icon_url= self.bot.user.avatar.url
        )

        # Fields :
        embed.add_field(name = "Add me to your server",
                        value = "[Click here to invite me \non your server](https://discord.com/oauth2/authorize?client_id=815328232537718794&permissions=1102128966768&scope=applications.commands+bot)",
                        inline = True)
        embed.add_field(name = "Vote me please",
                        value = "[You can vote me up on top.gg by \nclicking on this link](https://top.gg/bot/815328232537718794/vote)",
                        inline = True)

        await ctx.respond(embed = embed, ephemeral=True)


def setup(bot):
    print("Invite Command is ready !")
    bot.add_cog(InviteCommand(bot))
