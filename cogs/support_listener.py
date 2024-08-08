from discord import Embed
from discord.ext.commands import Cog

class SupportAssistance(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.user_id == 341257685901246466 :

            if payload.emoji.name == '✅':

                if payload.channel_id == 965009639991287879 :

                    EmbedContent = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

                    EmbedInfos = EmbedContent.embeds

                    EmbedSupportCheck = Embed(
                        title = "Support done !",
                        description = f"{EmbedInfos[0].description}",
                        color = 0x00ff00
                    )
                    EmbedSupportCheck.add_field(
                        name= f"{EmbedInfos[0].fields[0].name}",
                        value= f"{EmbedInfos[0].fields[0].value}",
                        inline=False
                    )

                    await EmbedContent.edit(embed = EmbedSupportCheck)



def setup(bot):
    print("Support Assistance is ready !")
    bot.add_cog(SupportAssistance(bot))
