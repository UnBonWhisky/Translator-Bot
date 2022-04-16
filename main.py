import discord
from discord import Intents
from discord.ext import commands,tasks
from discord.ext.commands import Bot, CommandNotFound
from discord.utils import get

from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

from datetime import timezone, tzinfo, timedelta, datetime
import sqlite3
import random
import asyncio
import os
import googletrans
from googletrans import Translator
import json
from urllib import request
from urllib.error import HTTPError

os.chdir(os.path.dirname(os.path.abspath(__file__)))

intents = discord.Intents(members=True, guilds=True, voice_states=True, presences=True, messages=True, reactions=True)

TOKEN = ''

client = commands.Bot(command_prefix = '%', intents=intents, activity = discord.Game(name=f"/ translations"))
client.remove_command('help')
slash = SlashCommand(client, sync_commands = True)

trad = Translator(service_urls=['translate.googleapis.com'])

db = sqlite3.connect('translator.sqlite')
cursor = db.cursor()

@client.event
async def on_ready():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS default_guild_language(
        guild_id TEXT,
        default_language TEXT,
        reaction_activated TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DMUser(
        user_id TEXT,
        yesno TEXT
        )
    """)

    for guild in client.guilds:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS guild{guild.id}(
            channel_id TEXT,
            channel_language TEXT
            )
        """)
    print("=== Translator Bot online ===")

@client.event
async def on_guild_join(guild):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS guild{guild.id}(
        channel_id TEXT,
        channel_language TEXT
        )
    """)
    
    botuser = client.get_user(815328232537718794)
    
    guildname = guild.name
    serveurlist = len(client.guilds)
    
    WEBHOOK_URL = ""

    payload = {
        'username': f'{botuser.name}',
        'avatar_url': f'{botuser.avatar_url}',
        'content' : '<@815328232537718794>',
        'embeds' : [
            {
                'title': 'Joined a guild',
                'description': f'I joined **{guildname}**. I am now on **{serveurlist}** servers',
                'color': 3066993,
                'timestamp': f'{datetime.utcnow()}',
            },
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
    }

    req = request.Request(url=WEBHOOK_URL,
                        data=json.dumps(payload).encode('utf-8'),
                        headers=headers,
                        method='POST')

    try:
        request.urlopen(req)
    except HTTPError as e:
        print('ERROR')
        print(e.reason)



@client.event
async def on_guild_remove(guild):
    
    botuser = client.get_user(815328232537718794)
    
    guildname = guild.name
    serveurlist = len(client.guilds)
    
    WEBHOOK_URL = ""

    payload = {
        'username': f'{botuser.name}',
        'avatar_url': f'{botuser.avatar_url}',
        'content' : '<@815328232537718794>',
        'embeds' : [
            {
                'title': 'Left a guild',
                'description': f'I left **{guildname}**. I am now on **{serveurlist}** servers',
                'color': 15158332,
                'timestamp': f'{datetime.utcnow()}',
            },
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
    }

    req = request.Request(url=WEBHOOK_URL,
                        data=json.dumps(payload).encode('utf-8'),
                        headers=headers,
                        method='POST')

    try:
        request.urlopen(req)
    except HTTPError as e:
        print('ERROR')
        print(e.reason)



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    

for filename in os.listdir(f"./cogs"):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(TOKEN)
