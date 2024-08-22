from discord import Embed, ApplicationContext, slash_command, option, InteractionContextType
from discord.ext.commands import Cog

class TranslateChoice(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name ="translatechoice",
        description = "Used to choose where you want your reaction translations.",
        contexts={InteractionContextType.guild}
    )
    @option(
        name="choice",
        description="Do you want your translations in DM or in the channel ?",
        required=True,
        type=str,
        choices=[
            "DM",
            "channel"
        ]
    )
    async def translatechoice(self, ctx : ApplicationContext, choice):
        
        await ctx.defer(ephemeral=True)

        await self.bot.cursor.execute(f"SELECT yesno FROM DMUser WHERE user_id = {ctx.author.id}")
        DMOnOff = await self.bot.cursor.fetchone()

        if choice == "DM" :
            EmbedMessage = Embed(
                description = "Reaction Translations will now be sent in your DMs !",
                color = 0x00ff00
            )
            if (DMOnOff is None) or (str(DMOnOff) == "(None,)"):
                pass
            else :
                sql = (f"DELETE FROM DMUser WHERE user_id = {ctx.author.id}")
                await self.bot.cursor.execute(sql)
                await self.bot.db.commit()
            
        else :
            EmbedMessage = Embed(
                description = "Reaction Translations will now be sent in the channel !",
                color = 0x00ff00
            )
            if DMOnOff is None:
                sql = ("INSERT INTO DMUser(user_id, yesno) VALUES(?,?)")
                val = (ctx.author.id, 1)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()
            elif str(DMOnOff) == "(None,)":
                sql = ("UPDATE DMUser SET yesno = ? WHERE user_id = ?")
                val = (1, ctx.author.id)
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()
        
        await ctx.respond(embed = EmbedMessage, ephemeral=True)


def setup(bot):
    print("Translate Choice Command is ready !")
    bot.add_cog(TranslateChoice(bot))
