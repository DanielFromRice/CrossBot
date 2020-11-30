# CrossBot
Discord bot for posting links to random crosswords


To Run: Must have .env file in the directory containing bot token. Current active bot is in CrossBotClient.py


CrossBot.py -> Bot to get crosswords using "Bot" class, uses prefix "+"

CrossBotClient.py -> Uses the more general "Client" class, more customizability in how to scan messages, this is the code currently in use. Responds to "crosswords?" anywhere in message

selenium_testing.py -> Implements logic of CrossBotClient for testing purposes

my_first_bot.py -> Implements a basic bot with random functionalities for testing purposes
