# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_NAME')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} has connected to Discord on the following guild:\n'
        f'{guild.name}(id: {guild.id})')
    members = guild.members
    print(f"\n Members: ({len(members)})")
    for member in members:
        print(f" - {member.name}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.__contains__("cross"):
        response = "Let's do a crossword!!! https://downforacross.com/"
        await message.channel.send(response)


client.run(TOKEN)
