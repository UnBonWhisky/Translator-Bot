from discord import Embed, ApplicationContext, slash_command, default_permissions, ButtonStyle, Interaction
from discord.ext.commands import Cog
from discord.ui import Button, View, button
import asyncio, aiosqlite

class ConfirmButton(View):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = None
        self.user = user

    @button(label="✅", style=ButtonStyle.blurple, custom_id=f"resetsettings_confirm")
    async def confirm_callback(self, button: Button, interaction: Interaction):
        if self.user.id == interaction.user.id:
            self.value = True
            self.stop()
        else:
            await interaction.response.send_message("Only the command author can use this button", ephemeral=True)
    
    async def on_timeout(self):
        self.value = False
        self.stop()
            

class ResetSettings(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(
        name="resetsettings",
        description="Erase all datas including channel languages and default language",
        guild_only=True
    )
    @default_permissions(administrator=True)
    async def resetsettings(self, ctx : ApplicationContext):
        
        await ctx.defer()

        Bouton = ConfirmButton(ctx.author, timeout=120)

        EmbedAreYouSure = Embed(
            description = "Are you sure you want to erase all datas of your server on the bot ?\nYou got 2 minutes to react",
            color = 0x8b0000
        )

        EmbedCancelled = Embed(
            description = "You didn't react in the 2 minutes given.\nReset task cancelled.",
            color = 0x5865F2
        )

        MessageSure = await ctx.respond(embed = EmbedAreYouSure, view=Bouton)

        await Bouton.wait()

        if (Bouton.value is False) or (Bouton.value is None):
            try :
                await MessageSure.edit(embed = EmbedCancelled, view=None)
            except :
                return
            return

        else:

            await self.bot.cursor.execute(f"DELETE FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
            await self.bot.db.commit()
            
            await self.bot.cursor.execute(f"DELETE FROM reversed WHERE guild_id = {ctx.guild.id}")
            await self.bot.db.commit()
            
            await self.bot.cursor.execute(f"DELETE FROM force_reaction WHERE guild_id = {ctx.guild.id}")
            await self.bot.db.commit()

            await self.bot.cursor.execute(f"DELETE FROM channel_language WHERE guild_id = {ctx.guild.id}")
            await self.bot.db.commit()

            await self.bot.cursor.execute(f"DELETE FROM linkchannels WHERE guild_id = {ctx.guild.id}")
            await self.bot.db.commit()
            
            await self.bot.cursor.execute(f"DELETE FROM langinfo WHERE guild_id = {ctx.guild.id}")
            await self.bot.db.commit()

            EmbedFinished = Embed(
                description = "All datas of your server has been erased !",
                color = 0x00ff00
                )

            await MessageSure.edit(embed = EmbedFinished, view=None)


def setup(bot):
    print("Reset Settings Command is ready !")
    bot.add_cog(ResetSettings(bot))
