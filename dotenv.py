"""
Idée pour head le Token ---> Surement inutile dans notre cas
"""


# This example requires the 'message_content' intent.
import logging
import discord
from discord import member
from dotenv import load_dotenv
import os
import re
from TokenList import list_token
from discord.ext import commands
from discord.utils import get

import json

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
load_dotenv(dotenv_path="METTRE LE LIENS VERS config.ini")


client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} est bien connecté au serveur.')


client.run(os.getenv("TOKEN"), log_handler=handler)
