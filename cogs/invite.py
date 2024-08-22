from discord import Embed, ApplicationContext, InteractionContextType
from discord.ext.commands import slash_command, Cog

class InviteCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "invite",
        description = "Anything you need to know if you want me on your server",
        contexts={InteractionContextType.guild}
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
                        value = "[Click here to invite me on your server or to install me to your profile](https://discord.com/oauth2/authorize?client_id=815328232537718794)",
                        inline = False)

        await ctx.respond(embed = embed, ephemeral=True)


def setup(bot):
    print("Invite Command is ready !")
    bot.add_cog(InviteCommand(bot))
