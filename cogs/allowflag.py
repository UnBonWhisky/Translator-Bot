from discord import Embed, option, ApplicationContext, default_permissions
from discord.ext.commands import slash_command, Cog
import aiosqlite

class ReactionFlag(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name ="allowflag",
        description = "Command for servers admins. Used to allow or not reactions flag on the server.",
        guild_only=True
    )
    @option(
        name="allowed",
        description="\"True\" to allow flag reactions on your server. \"False\" to don't allow.",
        required=False,
        type=bool
    )
    @option(
        name="force",
        description="\"none\" to have reactions flag in the user preference",
        required=False,
        type=str,
        choices=[
            "none",
            "DM",
            "channel"
        ]
    )
    @option(
        name="minimalist",
        description="\"True\" to return a minimalist version of flag reaction message. \"False\" get back to default one",
        required=False,
        type=bool
    )
    @option(
        name="timeout",
        description="Set up timeout on flag reaction messages (in seconds). \"0\" to get back to default",
        required=False,
        type=int
    )
    @default_permissions(administrator=True)
    async def allowflag(self, ctx : ApplicationContext, allowed = None, force = None, minimalist = None, timeout = None):
        
        await ctx.defer(ephemeral=True)

        EmbedDone = Embed(
            description = "Reaction flag setting has been set",
            color = 0x00ff00
        )

        # Check for allowed value
        if allowed is not None :
            if allowed is True:
                allowed = "enabled"
            elif allowed is False:
                allowed = "disabled"

        # Check for minimalist value
        if minimalist is not None :
            if minimalist is True :
                minimalist = "yes"
            elif minimalist is False :
                minimalist = "no"

        # Check for timeout value
        if timeout is not None :
            if timeout <= 0 :
                timeout = 0
        
        # check for allowed value
        if allowed is not None :
            await self.bot.cursor.execute(f"SELECT reaction_activated FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
            reaction_allowed = await self.bot.cursor.fetchone()

            if allowed == "enabled" :
                sql = (f"UPDATE default_guild_language SET reaction_activated = NULL WHERE guild_id = {ctx.guild.id}")
                await self.bot.cursor.execute(sql)
                await self.bot.db.commit()
            
            else :

                if str(reaction_allowed) == "None" and allowed == "disabled" :

                    sql = ("INSERT INTO default_guild_language(guild_id, reaction_activated) VALUES(?,?)")
                    val = (ctx.guild.id, allowed)

                else :
                
                    sql = ("UPDATE default_guild_language SET reaction_activated = ? WHERE guild_id = ?")
                    val = (allowed, ctx.guild.id)
                
                await self.bot.cursor.execute(sql, val)
                await self.bot.db.commit()
        
        # Check for force value
        if force is not None:

            await self.bot.cursor.execute(f"SELECT forced FROM force_reaction WHERE guild_id = {ctx.guild.id}")
            forced = await self.bot.cursor.fetchone()

            if force != "none":

                if str(forced) == "None":

                    sql = ("INSERT INTO force_reaction(guild_id, forced) VALUES(?,?)")
                    val = (ctx.guild.id, force)
                    await self.bot.cursor.execute(sql, val)
                    await self.bot.db.commit()

                else :

                    sql = ("UPDATE force_reaction SET forced = ? WHERE guild_id = ?")
                    val = (force, ctx.guild.id)
                    await self.bot.cursor.execute(sql, val)
                    await self.bot.db.commit()
            
            else :

                sql = (f"UPDATE force_reaction SET forced = NULL WHERE guild_id = {ctx.guild.id}")
                await self.bot.cursor.execute(sql)
                await self.bot.db.commit()
        

        # Check for minimalist value :
        if minimalist is not None :
            await self.bot.cursor.execute(f"SELECT minimalist FROM force_reaction WHERE guild_id = {ctx.guild.id}")
            minimalisted = await self.bot.cursor.fetchone()

            if minimalist == "no" :

                sql = (f"UPDATE force_reaction SET minimalist = NULL WHERE guild_id = {ctx.guild.id}")
                await self.bot.cursor.execute(sql)
                await self.bot.db.commit()
            
            else :

                if str(minimalisted) == "None" :
                    sql = ("INSERT INTO force_reaction(guild_id, minimalist) VALUES(?,?)")
                    val = (ctx.guild.id, minimalist)
                    await self.bot.cursor.execute(sql, val)
                    await self.bot.db.commit()

                else :

                    sql = ("UPDATE force_reaction SET minimalist = ? WHERE guild_id = ?")
                    val = (minimalist, ctx.guild.id)
                    await self.bot.cursor.execute(sql, val)
                    await self.bot.db.commit()

        # Check for timeout value :
        if timeout is not None :
            await self.bot.cursor.execute(f"SELECT timeout FROM force_reaction WHERE guild_id = {ctx.guild.id}")
            timeouted = await self.bot.cursor.fetchone()

            if timeout > 0 :

                if str(timeouted) == "None" :

                    sql = ("INSERT INTO force_reaction(guild_id, timeout) VALUES(?,?)")
                    val = (ctx.guild.id, str(timeout))
                    await self.bot.cursor.execute(sql, val)
                    await self.bot.db.commit()

                else :

                    sql = ("UPDATE force_reaction SET timeout = ? WHERE guild_id = ?")
                    val = (str(timeout), ctx.guild.id)
                    await self.bot.cursor.execute(sql, val)
                    await self.bot.db.commit()
            
            else :

                sql = (f"UPDATE force_reaction SET timeout = NULL WHERE guild_id = {ctx.guild.id}")
                await self.bot.cursor.execute(sql)
                await self.bot.db.commit()

        await ctx.respond(embed = EmbedDone, ephemeral=True)



def setup(bot):
    print("Allow Flag Command is ready !")
    bot.add_cog(ReactionFlag(bot))