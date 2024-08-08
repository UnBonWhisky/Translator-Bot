import discord
from discord import Embed, ApplicationContext
from discord.ext.commands import slash_command, Cog
from datetime import datetime

class StatsCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="stats",
        description="Display the stats of the bot.",
        guild_only=True
    )
    async def stats(self, ctx: ApplicationContext):
        
        await ctx.defer(ephemeral=True)

        uptime = datetime.now() - self.bot.start_time
        days, remainder = divmod(int(uptime.total_seconds()), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = Embed(
            title="Stats Command",
            description="They are the stats of my bot.",
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
            name="Servers",
            value="{:,}".format(len(self.bot.guilds)).replace(',', ' '),
            inline=True
        )
        embed.add_field(
            name="Channels",
            value="{:,}".format(sum(len(guild.channels) for guild in self.bot.guilds)).replace(',', ' '),
            inline=True
        )
        embed.add_field(
            name="Users",
            value="{:,}".format(sum(guild.member_count for guild in self.bot.guilds)).replace(',', ' '),
            inline=True
        )
        embed.add_field(
            name="Actual Server Shard :",
            value=ctx.guild.shard_id,
            inline=True
        )
        embed.add_field(
            name="Uptime :",
            value=f"{days}d {hours}h {minutes}m {seconds}s",
            inline=True
        )
        embed.add_field(
            name="Shards count :",
            value=self.bot.shard_count,
            inline=True
        )

        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    print('Stats Command is ready!')
    bot.add_cog(StatsCommand(bot))
