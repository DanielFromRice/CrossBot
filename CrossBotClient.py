import os
from dotenv import load_dotenv
import discord
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random
import re
import sys

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_NAME')

phrases = [
    "You deserve a crossword",
    "It'll only take a few minutes...",
    "Nicky would want you to do it",
    "This one should be a challenge",
    "Have fun!!!",
    "Don't get bamboozled....",
    "Take a look at these squares!",
    "These clues might be tricky",
    "Ooh, a crossword!"
]

num_phrases = len(phrases)

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord on the following guilds:')
    for guild in client.guilds:
        print(f'{guild.name}  (id: {guild.id})')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    txt = message.content

    cross_compare = re.compile("[cC]rossword\?")
    if not cross_compare.search(txt) is None:

        browser = webdriver.Firefox()
        browser.get("https://downforacross.com/")
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "entry--container"))
            )
        finally:
            puzzles = browser.find_elements_by_class_name("entry--container")
        puzzle_selection = puzzles[random.randint(0, len(puzzles))]
        puzzle_selection.click()
        try:
            element2 = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "chat--header--title"))
            )
        finally:
            phrase = phrases[random.randint(0, num_phrases-1)]
            response = f"{phrase}: \n {browser.current_url}"
        await message.channel.send(response)
        browser.quit()


client.run(TOKEN)
