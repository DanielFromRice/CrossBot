# UltimateBot.py
import os

import discord
from discord.ext import commands
from PIL import Image
import io
from dotenv import load_dotenv
import UltimateGame

import json

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='ultimate.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('TIC_TAC_TOKEN')
GUILD = os.getenv('GUILD_NAME')

intents = discord.Intents.default()
intents.members = True
ticBot = commands.Bot(command_prefix="XO.", intents=intents)

game_data = {}
# game_data{player : {opponent: (name), moves: [moves], turn: (bool), sym : (X or O)} }

file = "ultTest1.txt"


async def index_files():
    global game_data
    if os.path.exists(f"TicTacData/{file}"):
        with open(f"TicTacData/{file}", 'r') as fil:
            in_str = fil.readlines()[0]
        json_data = json.loads(in_str)
        game_data = json_data
    else:
        game_data = {}


async def write_data():
    print(json.dumps(game_data))
    with open("TicTacData/ultimate_data.txt", 'w') as fil:
        fil.write(json.dumps(game_data))


@ticBot.event
async def on_ready():
    await index_files()
    print(f'{ticBot.user} has connected to Discord on the following guilds:')
    for guild in ticBot.guilds:
        print(f'{guild.name}  (id: {guild.id})')


@ticBot.command(name="new", help="Start a new Tic Tac Toe Game")
async def new_game(ctx, member_in: discord.Member):
    global game_data
    player1 = ctx.message.author
    player2 = member_in
    if player1.id == player2.id:
        raise commands.BadArgument("Same")
    elif str(player1.id) in game_data.keys() and str(player2.id) in game_data[str(player1.id)]:
        raise commands.BadArgument("P1")
    else:
        # await ctx.message.channel.send(f"You are person {player1.id}")
        # await ctx.message.channel.send(f"Your username is {player1}")
        # await ctx.message.channel.send(f"Your opponent is {player2.id}")
        # await ctx.message.channel.send(f"Their username is {player2}")
        move_list = []
        sector_statuses = {key: "N" for key in range(9)}
        if game_data.keys().__contains__(str(player1.id)):
            game_data[str(player1.id)][str(player2.id)] = {"moves": move_list, "turn": True, "sym": "X", "secs": sector_statuses}
        else:
            game_data[str(player1.id)] = {str(player2.id): {"moves": move_list, "turn": True, "sym": "X", "secs": sector_statuses}}
        if game_data.keys().__contains__(str(player2.id)):
            game_data[str(player2.id)][str(player1.id)] = {"moves": move_list, "turn": False, "sym": "O", "secs": sector_statuses}
        else:
            game_data[str(player2.id)] = {str(player1.id): {"moves": move_list, "turn": False, "sym": "O", "secs": sector_statuses}}
        print(game_data)
        await ctx.message.delete()
        img = UltimateGame.draw_game([], sector_statuses)
        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send("----------------------------------------------")
            await ctx.send(f"New Game! {player1} is X's, {player2} is O's.")
            await ctx.send(file=discord.File(fp=image_binary, filename='latest_turn.png'))
            await ctx.send(f"{player1}, it is your turn!")


@new_game.error
async def new_game_error(ctx, err):
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send(
            "Sorry, couldn't figure out who you want to play with! Please include all "
            "appropriate arguments in the form: \n> XO.new [@player_name]")
    elif isinstance(err, commands.BadArgument):
        if str(err) == "P1":
            await ctx.send(f"{ctx.message.author}, you already have a game active with this player! Finish or quit your current game to start a new one")
        elif str(err) == "Same":
            await ctx.send(f"You can't play a game with yourself!")
    else:
        print(err)


@ticBot.command(name="play", help="Play your turn!")
async def play(ctx, sector: int, space: int, opponent: discord.Member):
    player = ctx.message.author

    if not game_data.keys().__contains__(str(player.id)) or not game_data.keys().__contains__(str(opponent.id)) or not \
            game_data[str(player.id)].keys().__contains__(str(opponent.id)) or not game_data[str(opponent.id)].keys().__contains__(str(player.id)):
        raise commands.MemberNotFound("No Game Active")
    if not game_data[str(player.id)][str(opponent.id)]["turn"]:
        raise commands.BadBoolArgument("Not your turn")
    if space < 1 or space > 9 or sector < 1 or sector > 9:
        raise commands.ArgumentParsingError("Bad Space")

    moves = game_data[str(player.id)][str(opponent.id)]["moves"]
    if len(moves) == 0:
        pass
    else:
        assigned_sector = moves[len(moves)-1][2]
        print(moves)
        used_spaces = [move[2] for move in moves if move[1] == assigned_sector]
        if len(used_spaces) < 9:
            if assigned_sector != sector - 1:
                print(f"{assigned_sector}, {sector}")
                raise commands.ArgumentParsingError("Wrong Sector")
            if (space - 1) in used_spaces:
                raise commands.ArgumentParsingError("Used Space")

    moves.append([game_data[str(player.id)][str(opponent.id)]['sym'], sector - 1, space - 1])
    changed_sector = [[move[0], move[2]] for move in moves if move[1] == sector - 1]
    sector_win = UltimateGame.check_win(changed_sector)
    winner = "N"
    if sector_win != "N":
        game_data[str(player.id)][str(opponent.id)]["secs"][sector - 1] = sector_win
        game_data[str(opponent.id)][str(player.id)]["secs"][sector - 1] = sector_win
        sector_list = [[sym, sec] for sec, sym in game_data[str(player.id)][str(opponent.id)]["secs"] if sym != "N"]
        print(sector_list)
        winner = UltimateGame.check_win(sector_list)

    if winner == "N":
        img = UltimateGame.draw_game(moves, game_data[str(player.id)][str(opponent.id)]["secs"])
        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(f"----------------------------------------------")
            await ctx.send(f"{ctx.message.author} just played an {game_data[str(player.id)][str(opponent.id)]['sym']}!", file=discord.File(fp=image_binary, filename='latest_turn.png'))
            await ctx.send(f"{opponent}, it is your turn!")
        await ctx.message.delete()
        game_data[str(player.id)][str(opponent.id)]["turn"] = False
        game_data[str(opponent.id)][str(player.id)]["turn"] = True
        game_data[str(player.id)][str(opponent.id)]["moves"] = moves
        game_data[str(opponent.id)][str(player.id)]["moves"] = moves
    else:
        img = UltimateGame.draw_game(moves, game_data[str(player.id)][str(opponent.id)]["secs"])
        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(f"{winner}'s won! Congratulations {player}!! Better luck next time, {opponent}",
                           file=discord.File(fp=image_binary, filename='latest_turn.png'))
        await ctx.message.delete()
        game_data[str(player.id)].pop(str(opponent.id))
        game_data[str(opponent.id)].pop(str(player.id))
    await write_data()


@play.error
async def play_error(ctx, err):
    if isinstance(err, commands.MemberNotFound):
        await ctx.send("You don't have an active game!")
    elif isinstance(err, commands.BadBoolArgument):
        await ctx.send(f"{ctx.message.author}, it's not your turn!")
    elif isinstance(err, commands.ArgumentParsingError):
        if str(err) == "Wrong Sector":
            await ctx.send(f"Might want to rethink that one! You are trying to play in the wrong sector! \nRemember to write your move as XO.play <big_grid> <small_grid> @<opponent>")
        else:
            await ctx.send(f"You can't play on that space!")
    elif isinstance(err, commands.MissingRequiredArgument):
        await ctx.send(f"Please try again! You're missing an argument...")
    else:
        await ctx.send(f"Something went wrong, sorry.....")
        print(type(err))


@ticBot.command(name="game_info", help="Current information about your active game")
async def game_info(ctx):
    global game_data
    player = ctx.message.author
    if str(player.id) in game_data.keys():
        if len(game_data[str(player.id)]) > 0:
            await ctx.send(f"Hi {player}! You have the following active games:")
            for opp_id in game_data[str(player.id)]:
                if game_data[str(player.id)][str(opp_id)]["turn"]:
                    whose_turn = "your"
                else:
                    whose_turn = "their"
                img = UltimateGame.draw_game(game_data[str(player.id)][str(opp_id)]["moves"], game_data[str(player.id)][str(opp_id)]["secs"])
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(f"You are currently playing {ticBot.get_user(int(opp_id))} and it is {whose_turn} turn. You are playing as {game_data[str(player.id)][opp_id]['sym']}.")
                    await ctx.send(file=discord.File(fp=image_binary, filename="latest_turn.png"))
        else:
            await ctx.send(f"{player}, you have no active games!")
    else:
        await ctx.send(f"{player}, you have no active games!")


@ticBot.command(name="quit", help="Quits a current game")
async def quit(ctx, other_player: discord.Member):
    player = ctx.message.author
    if game_data[str(player.id)].__contains__(str(other_player.id)):
        game_data[str(other_player.id)].pop(str(player.id))
        game_data[str(player.id)].pop(str(other_player.id))
        await ctx.send(f"{player}, you have quit your game against {other_player}")
        await write_data()
    else:
        await ctx.send(f"{player}, you aren't currently playing against {other_player}!")


ticBot.run(TOKEN)

