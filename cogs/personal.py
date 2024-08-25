from discord import slash_command, ApplicationContext, AutocompleteContext, option, Embed, InteractionContextType, IntegrationType
from discord.ext.commands import Cog
from googletrans import LANGNAMES
from main import translator_handler

LANGUAGES = list(LANGNAMES) # Pour créer une copie de la liste
if 'none' not in LANGUAGES:
    LANGUAGES.insert(0, 'none')

class PersonalCommand(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def get_languages(ctx: AutocompleteContext):
        filtered_languages = [lang for lang in LANGUAGES if lang.startswith(ctx.value.lower())]
        if len(filtered_languages) > 25:
            return filtered_languages[:25]
        else:
            return filtered_languages
    
    @slash_command(
        name="personal",
        description="Use this command to set your personal language for `Translate` in the App Menu.",
        contexts = {
            InteractionContextType.guild,
            InteractionContextType.private_channel,
            InteractionContextType.bot_dm,
        },
        integration_types = {
            IntegrationType.guild_install,
            IntegrationType.user_install,
        }
    )
    @option(
        name="language",
        description="The language you want to translate your text into. `none` to reset.",
        required=True,
        type=str,
        autocomplete=get_languages
    )
    @translator_handler
    async def personal(self, ctx : ApplicationContext, language):
        await ctx.defer(ephemeral=True)
        
        if language not in LANGUAGES :
            await ctx.respond("This language is not supported.", ephemeral=True)
            return

        cursor = await self.bot.db.cursor()
        
        if language != 'none' :
            EmbedMessage = Embed(
                description = f"Your personal language has been set to {language}.",
                color = 0x5865F2
            )
            await cursor.execute(f"SELECT language FROM personal_language WHERE user_id = {ctx.author.id}")
            result = await cursor.fetchone()
            
            if result :
                await cursor.execute(f"UPDATE personal_language SET language = '{language}' WHERE user_id = {ctx.author.id}")
            else :
                sql = ("INSERT INTO personal_language(user_id, language) VALUES(?,?)")
                val = (ctx.author.id, language)
                await cursor.execute(sql, val)
        
        else :
            EmbedMessage = Embed(
                description = f"Your personal language has deleted.\nIt will now use the discord client language.",
                color = 0x5865F2
            )
            await cursor.execute(f"DELETE FROM personal_language WHERE user_id = {ctx.author.id}")
        
        await self.bot.db.commit()
        await cursor.close()

        await ctx.respond(embed = EmbedMessage, ephemeral=True)
        
        


def setup(bot):
    print("Personal Command is ready !")
    bot.add_cog(PersonalCommand(bot))