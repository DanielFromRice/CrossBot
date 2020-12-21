### Deprecated, use TicTacToeBot ###

import os

import discord
from PIL import Image
import io
from dotenv import load_dotenv
import TicTacToeGame

load_dotenv()
TOKEN = os.getenv('TIC_TAC_TOKEN')
GUILD = os.getenv('GUILD_NAME')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord on the following guilds:')
    for guild in client.guilds:
        print(f'{guild.name}  (id: {guild.id})')
    guild = discord.utils.get(client.guilds, name=GUILD)
    members = guild.members
    # print(f"\n Members: ({len(members)})")
    for member in members:
        print(f" - {member.name}")

@client.event
async def on_message(message, member_in: discord.Member):
    if message.author == client.user:
        return

    if message.content[0:4] == "XOXO":
        # await message.channel.send(f"{message.author} just played:", file=discord.File('sample_imgs/tic_tac1.png'), )
        stuff = message.content.split(" ")
        if len(stuff) < 2:
            await message.channel.send("You have too few arguments!!")
        if stuff[1] == "new":
            # new_msg_list = []
            player1 = message.author.id
            # player2 = message.guild.get_member("RachRocks#1973")
            print(member_in)
            await message.channel.send(f"You are person {player1}")
            await message.channel.send(f"Your username is {message.guild.get_member(player1)}")
        else:
            img = TicTacToeGame.draw_game(["Player1", "Player2", 'x;2', 'o;4', 'x;1'])
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                await message.channel.send(f"{message.author} just played!!!", file=discord.File(fp=image_binary, filename='latest_turn.png'))
            # await message.channel.send(file=discord.File())
        await message.delete()


client.run(TOKEN)
