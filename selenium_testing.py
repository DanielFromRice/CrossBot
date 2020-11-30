from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random

import sys

puzzle_num = -1

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
# anchor = puzzle_selection.find_element_by_css_selector("a:nth-child(1)")
puzzle_selection.click()
try:
    element2 = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "chat--header--title"))
    )
finally:
    print(browser.current_url)
# print(puzzle_selection.tag_name)
# print(anchor.tag_name)
# print(anchor.get_attribute("href"))
browser.quit()