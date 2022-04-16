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

@client.event
async def on_guild_remove(guild):
    cursor.execute(f"SELECT default_language FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
    DefaultLG = cursor.fetchone()

    if str(DefaultLG) == "None" or str(DefaultLG) == "(None,)":
        pass

    else :

        cursor.execute(f"DELETE FROM default_guild_language WHERE guild_id = {ctx.guild.id}")
        db.commit()
    
    cursor.execute(f"SELECT * FROM guild{ctx.guild.id}")
    ischannelinlist = cursor.fetchall()

    if str(ischannelinlist) == "None" or str(ischannelinlist) == "(None,)" :
        pass

    else :

        cursor.execute(f"DELETE FROM guild{ctx.guild.id}")
        db.commit()
    
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    

for filename in os.listdir(f"./cogs"):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(TOKEN)
