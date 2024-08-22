from discord import slash_command, ApplicationContext, Embed, InteractionContextType
from discord.ext.commands import Cog

class ServerStats(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(
        name="serverstats",
        description="Prints all configured informations on the server",
        contexts={InteractionContextType.guild}
    )
    async def serverstats(self, ctx: ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        await self.bot.cursor.execute(f"SELECT * FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
        default_guild_language = await self.bot.cursor.fetchall()
        
        await self.bot.cursor.execute(f"SELECT * FROM reversed WHERE guild_id = {ctx.guild.id}")
        reversed = await self.bot.cursor.fetchall()
        
        await self.bot.cursor.execute(f"SELECT * FROM force_reaction WHERE guild_id = {ctx.guild.id}")
        force_reaction = await self.bot.cursor.fetchall()

        await self.bot.cursor.execute(f"SELECT * FROM channel_language WHERE guild_id = {ctx.guild.id}")
        channel_language = await self.bot.cursor.fetchall()

        await self.bot.cursor.execute(f"SELECT * FROM linkchannels WHERE guild_id = {ctx.guild.id}")
        linkchannels = await self.bot.cursor.fetchall()
        
        await self.bot.cursor.execute(f"SELECT * FROM langinfo WHERE guild_id = {ctx.guild.id}")
        langinfo = await self.bot.cursor.fetchall()

        EmbedMessage = Embed(
            title = "Here are the server stats",
            description = "If the information is not displayed, it means there is no configuration of it on this server",
            color = 0x5865F2
        )

        if default_guild_language != []:
            EmbedMessage.add_field(
                name="Default Guild Language",
                value=f"The default language {'is set to ' + default_guild_language[0][1] if default_guild_language[0][1] else 'is not set'} and flag reactions are {'disabled' if default_guild_language[0][2] is not None else 'enabled'}.",
                inline=False
            )
        
        if channel_language != []:
            EmbedMessage.add_field(
                name="Channel Languages",
                value=f"There is {len(channel_language)} channel languages configured.",
                inline=False
            )
        
        if reversed != []:
            EmbedMessage.add_field(
                name="Reversed",
                value=f"There is {len(reversed)} reversed languages configured.",
                inline=False
            )
        
        if linkchannels != []:
            EmbedMessage.add_field(
                name="Link Channels",
                value=f"There is {len(linkchannels)} link channels configured.",
                inline=False
            )
        
        if force_reaction != []:
            EmbedMessage.add_field(
                name="Flag Reactions",
                value=f"Flag reactions are {'not enforced' if force_reaction[0][1] is None else 'enforced in ' + force_reaction[0][1]}.\nMinimalist mode is {'enabled' if force_reaction[0][2] == 'yes' else 'disabled'}.\nThe timeout is {'not set' if force_reaction[0][3] is None else force_reaction[0][3] + ' seconds'}.",
                inline=False
            )
        
        if langinfo != []:
            EmbedMessage.add_field(
                name="Language Infos",
                value=f"Language informations are enabled.",
                inline=False
            )

        await ctx.respond(embed=EmbedMessage, ephemeral=True)
        
        


def setup(bot):
    print("Server Stats Command is ready !")
    bot.add_cog(ServerStats(bot))
    
