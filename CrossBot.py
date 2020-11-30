import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_NAME')

crossbot = commands.Bot(command_prefix = "+")

@crossbot.event
async def on_ready():
    print(f'{crossbot.user} has connected to Discord on the following guilds:\n')
    for guild in crossbot.guilds:
        print(f'{guild.name}(id: {guild.id})')

@crossbot.command(name = "site", help = "Pull up a crossword puzzle!")
async def puz(ctx, puzzle: int = -1):
    response = "https://downforacross.com/"
    await ctx.send(response)


@crossbot.command(name = "puzzle", help = "Makes a new crossword puzzle!")
async def new_puz(ctx, puzzle_num: int = -1):
    browser = webdriver.Firefox()
    browser.get("https://downforacross.com/")
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "entry--container"))
        )
    finally:
        puzzles = browser.find_elements_by_class_name("entry--container")
    if puzzle_num == -1 or puzzle_num >= len(puzzles):
        puzzle_selection = puzzles[random.randint(0, len(puzzles))]
    else:
        puzzle_selection = puzzles[puzzle_num]
    puzzle_selection.click()
    try:
        element2 = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "chat--header--title"))
        )
    finally:
        await ctx.send(browser.current_url)
    browser.quit()

crossbot.run(TOKEN)
