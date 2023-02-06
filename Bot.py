# This example requires the 'message_content' intent.
"""
import logging
from typing import Optional, Any
from discord.utils import get
from discord import member
from discord import member
from dotenv import load_dotenv
import os
import re
"""
import asyncio

from discord.ext import commands
import discord
from TokenList import list_token
from CmdList import cmd_list

"""
Création de la variable contenant le token du bot.
Connexion Bot
"""

with open("venv/token.txt", 'r') as file:
    key_token = file.read()

"""
Création de la variable bot qui nous servira tout le long. l'argument 'command_prefix' définit le prefix à mettre devant
les commandes discord
"""

bot = commands.Bot(instant=discord.Intents.all(), description="Le Bot de la Solution", command_prefix="*")

"""
@bot.Event annonce une fonction évènement ici la connection du bot au serveur discord. Ex: un nouvelle utilisateur se 
 connecte au serveur discord
"""


@bot.event
async def on_ready():
    print("MyBot est connecté")


"""
@bot.command() annonce une fonction commande discord, afin de créé une nouvelle commande discord
"""


@bot.command()
async def ping(ctx):
    await ctx.send("Pong !")
    await ctx.message.delete()


@bot.command()
async def latence(ctx):
    await ctx.send(f"la latence du Bot est de: {round(bot.latency * 1000)} ms.")


@bot.command()
async def commander(ctx):
    await ctx.send("Que souhaitez-vous ?")

    def check_message(_message):
        return _message.author == ctx.message.author and ctx.message.channel == _message.channel

    try:
        commande = await bot.wait_for("message", timeout=30, check=check_message)
    except (asyncio.exceptions.TimeoutError, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("Vous avez été trop long à répondre, recommencer s'il vous plait")
        return
    message = await ctx.send(
        f"Voulez vous validé cette demande ({commande.content}) ? Cochez ✅ pour valider, ou cocher ❌ pour annuler")
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def check_emoji(_reaction, _user):
        return ctx.message.author == _user and message.id == _reaction.message.id and (
                str(_reaction.emoji) == "✅" or str(_reaction.emoji) == "❌")

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30, check=check_emoji)
        if reaction.emoji == "✅":
            await ctx.send("Votre demande a été confirmé")
        if reaction.emoji == "❌":
            await ctx.send("Votre demande a été annulé")

    except (asyncio.exceptions.TimeoutError, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("Vous avez été trop long à répondre, recommencer s'il vous plait")
        return


@bot.command()
async def token(ctx):
    """
    Créé la command token pour ajouter le role authenticated si le token correspond a la 'TokenList.py'
    """
    await ctx.send("Veuillez entré votre Usertoken")

    def check_message(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel

    try:
        usertoken = await bot.wait_for("message", timeout=10, check=check_message)
        await ctx.message.delete()
    except (asyncio.exceptions.TimeoutError, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("Vous avez été trop long à répondre, recommencer s'il vous plait")
        await ctx.message.delete()
        return

    if usertoken.content in list_token:
        await ctx.send("Félicitation, vous êtes bien authentifié !")
        authenticated = discord.utils.get(ctx.guild.roles, id=1031169627478294568)
        await ctx.author.add_roles(authenticated, reason="MyBot à authentifier ")

    else:
        await ctx.send("Ce UserToken n'est pas reconnu.")

    await usertoken.delete()


@bot.command()
@commands.has_role('Admin')
async def remove_token_role(ctx, user: discord.Member):
    """
    Créé la command remove_token_role pour supprimer le role authenticated (utilisable seulement si role 'Admin')
    """
    authenticated = discord.utils.get(ctx.guild.roles, id=1031169627478294568)
    await user.remove_roles(authenticated, reason="L'utilisateur n'est plus abonné.")
    await ctx.send(f"{user.name} n'est plus authentifié.")
    await ctx.message.delete()


@bot.command()
@commands.has_role('Admin')  # permet de définir qu'elle role peut utiliser la command
async def version(ctx):
    """
    Créé la command version pour afficher la version de  MyBot Inscrit a la variable 'version_bot'
    """
    version_bot = "1.0"
    await ctx.send(f"La version de **MyBot** est **{version_bot}** .")
    await ctx.message.delete()


@bot.command()
async def helper(ctx):
    """
    Créé la command helper pour afficher la list des command disponible (la commande '*help' existe par default, ici
    commande affiche la list sous forme d'un 'Embed'
    """
    saut = "\n"
    helper = discord.Embed(title="Liste des commandes disponibles :", description=f"{saut.join(cmd_list)}",
                           colour=0xF9F7A1)
    helper.set_author(name="MytyBot")

    await ctx.send(embed=helper)
    await ctx.message.delete()

if __name__ == "__main__":
    bot.run(key_token)
