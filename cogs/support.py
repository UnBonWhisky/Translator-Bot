import time
from discord import Embed, ApplicationContext, option, default_permissions
from discord.ext.commands import slash_command, Cog

class SupportCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name ="support",
        description = "Need help about anything on the bot ? Join the support server.",
        guild_only=True
    )
    @option(
        name="message",
        description="Message of your problem. If your message is not precise, it will be ignored.",
        required=True,
        opt_type=str
    )
    @default_permissions(administrator=True)
    async def support(self, ctx : ApplicationContext, message):
        
        await ctx.defer()

        infojour = time.strftime("%H:%M:%S %d/%m/%Y")

        EmbedMessageSent = Embed(title = "Sent !",
                                        description = "Your request has been sent. Check your discord friend invitations.\nThe bot owner will add you as friend if he need it !\nGo check on the [bot owner server](https://discord.gg/gqfFqJp) to know when your support help is done !",
                                        color = 0x00ff00
                                        )
        EmbedMessageSent.add_field(name = "Your message :",
                                value = f"{message}",
                                inline = False)
        EmbedMessageSent.add_field(name="Other contact methods",
                                value="Discord : unbonwhisky\nGithub : [UnBonWhisky](https://github.com/UnBonWhisky)",
                                inline = False)

        EmbedSupportRequest = Embed(title = "Support Required !",
                                                description = f"**Ticket opened by :**\n`{ctx.author} / {ctx.author.id}`\n\n**Guild :**\n{ctx.guild.name} / {ctx.guild.id}\n\n**Date / Time of the message :**\n{infojour}",
                                                color = 0xff0000
                                                )
        EmbedSupportRequest.add_field(name="Support Message :",
                                    value=f"{message}",
                                    inline=False)

        channel_send = await self.bot.fetch_channel(965009639991287879)
        await channel_send.send(embed = EmbedSupportRequest)
        await ctx.respond(embed = EmbedMessageSent)



def setup(bot):
    print("Support Command cog ready !")
    bot.add_cog(SupportCommand(bot))
