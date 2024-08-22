from discord import Embed, ApplicationContext, InteractionContextType
from discord.ext.commands import Cog, slash_command

class DonationCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name = "donation",
        description = "If you want to thank me for my work :)",
        contexts={InteractionContextType.guild}
    )
    async def donation(self, ctx : ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        EmbedDonation = Embed(title = "Wanna support me ?",
                                    description = "it would help me a lot if you have the possibility to donate to me :\nOne time with [Buy me a coffee](https://www.buymeacoffee.com/UnBonWhisky)\nEach month with [Patreon](https://www.patreon.com/JeSuisUnBonWhisky)\nI can give you a paypal link with adding me as friend and send me a DM ( `unbonwhisky` )\n\nMy goal would be to earn a total of 120 € to have new stuff to host my bots\nThank you in advance,\n**unbonwhisky**",
                                    color = 0xf1c40f)

        await ctx.respond(embed = EmbedDonation, ephemeral=True)


def setup(bot):
    print("Donation Command is ready !")
    bot.add_cog(DonationCommand(bot))
