import discord, aiosqlite, os, json, httpx, random
from discord import Intents
from discord.ext import tasks
from dotenv import load_dotenv
from datetime import datetime
from googletrans import Translator, LANGUAGES, FLAG_CODES, LANGKEYS, LANGNAMES, LANGCODES, RateLimitError
from functools import wraps

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Chargement du token
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Création du Httpx client
client = httpx.AsyncClient()

class ShardedBot(discord.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.cursor = None
        self.trad = None
        self.LANGUAGES = LANGUAGES
        self.FLAG_CODES = FLAG_CODES
        self.LANG_KEYS = LANGKEYS
        self.LANG_NAMES = LANGNAMES
        self.LANGCODES = LANGCODES
    
    async def start(self, token: str, *, reconnect: bool = True):
        await self.setup_database()
        await self.setup_translator()
        
        # Load cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.{filename[:-3]}')
                
        await self.login(token)
        await self.connect(reconnect=reconnect)
        
    
    # On connection function
    async def setup_database(self):
        # Connect to the database and create the cursor for adding into the db
        self.db = await aiosqlite.connect('translator.sqlite')
        self.cursor = await bot.db.cursor()
        
        await self.create_tables()

    async def setup_translator(self):
        
        proxy="[PRIVATE]"
        
        self.trad = Translator(proxy=proxy)
        print("=== Proxy Setup updated ! ===")
        
    @staticmethod
    def translator_handler(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except RateLimitError:
                await self.setup_translator()
                try:
                    return await func(self, *args, **kwargs)
                except RateLimitError:
                    raise RateLimitError("Rate limit error even after changing proxy.")
        return wrapper
        
    async def create_tables(self):
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS default_guild_language(
            guild_id TEXT,
            default_language TEXT,
            reaction_activated TEXT
            )
        """)
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS DMUser(
            user_id TEXT,
            yesno TEXT
            )
        """)
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reversed(
            guild_id TEXT,
            channel_id TEXT,
            language_1 TEXT,
            language_2 TEXT
            )
        """)
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS channel_language(
            guild_id TEXT,
            channel_id TEXT,
            language TEXT
            )
        """)
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS force_reaction(
            guild_id TEXT,
            forced TEXT,
            minimalist TEXT,
            timeout TEXT
            )
        """)
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS linkchannels(
            guild_id TEXT,
            channel_id_1 TEXT,
            channel_id_2 TEXT,
            language_1 TEXT,
            language_2 TEXT,
            webhook_1 TEXT,
            webhook_2 TEXT
            )
        """)
        await self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS langinfo(
            guild_id TEXT,
            info TEXT
            )
        """)
        print('=== Database Tables are created ! ===')
        
    
    # On ready
    async def on_ready(self):
        print('===== Translator Bot is ready ! =====')

    # On shard connect
    async def on_shard_connect(self, shard_id):
        print(f"=== Shard {shard_id}/{bot.shard_count-1} is ready ! ===")

intents = Intents(guilds=True, messages=True, reactions=True, message_content=True, voice_states=True)
bot = ShardedBot(intents=intents, activity=discord.Game(name="/ translations"), owner_id=341257685901246466)
bot.start_time = datetime.now()

# On guild join
@bot.event
async def on_guild_join(guild):
    
    if guild.name is None:
        return

    guildname = guild.name
    botuser = bot.user
    serveurlist = "{:,}".format(len(bot.guilds)).replace(',', ' ')

    WEBHOOK_URL = "[PRIVATE]"

    payload = {
        'username': f'{botuser.display_name}',
        'avatar_url': f'{botuser.avatar.url}',
        'content' : f'<@815328232537718794> Joined - {serveurlist}',
        'embeds' : [
            {
                'title': 'Joined a guild',
                'description': f'I joined **{guildname}**. I am now on **{serveurlist}** servers',
                'color': 3066993,
            },
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
    }

    await client.post(url=WEBHOOK_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers
    )

# On guild leave
@bot.event
async def on_guild_remove(guild):
    if guild.name is None :
        return
    
    await bot.cursor.execute(f"DELETE FROM channel_language WHERE guild_id = {guild.id}")
    await bot.db.commit()

    await bot.cursor.execute(f"DELETE FROM default_guild_language WHERE guild_id = {guild.id}")
    await bot.db.commit()

    await bot.cursor.execute(f"DELETE FROM reversed WHERE guild_id = {guild.id}")
    await bot.db.commit()
    
    guildname = guild.name
    botuser = bot.user
    serveurlist = "{:,}".format(len(bot.guilds)).replace(',', ' ')

    WEBHOOK_URL = "[PRIVATE]"

    payload = {
        'username': f'{botuser.name}',
        'avatar_url': f'{botuser.avatar.url}',
        'content' : f'<@815328232537718794> Left - {serveurlist}',
        'embeds' : [
            {
                'title': 'Left a guild',
                'description': f'I left **{guildname}**. I am now on **{serveurlist}** servers',
                'color': 15158332,
            },
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
    }

    await client.post(url=WEBHOOK_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers
    )

if __name__ == '__main__':
    bot.run(TOKEN)