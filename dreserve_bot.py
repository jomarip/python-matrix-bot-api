"""
A test bot using the Python Matrix Bot API

Test it out by adding it to a group chat and doing one of the following:
1. Respond to greetings aloha, hi and hello
2. Say !echo this is a test!
3. Say !d6 to get a random size-sided die roll result
"""

import random

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler

# Global variables
USERNAME = ""  # Bot's username
PASSWORD = ""  # Bot's password
SERVER = "http://matrix.org"  # Matrix server URL

adios=["aloha","hi","hello"]				#create a list of words


def hi_callback(room, event):
    # Somebody said hi, let's say Hi back
    args = event['content']['body'].split()      #find the words in the message body
    try:
        print(adios.index(' '.join(set(adios)&set(args))))       #find the index value for the message body words which match the list
    except ValueError:
        print("No Match")
    room.send_text("Hi, " + event['sender'])
	


def echo_callback(room, event):
    args = event['content']['body'].split()
    args.pop(0)

    # Echo what they said back
    room.send_text(' '.join(args))


def dieroll_callback(room, event):
    # someone wants a random number
    args = event['content']['body'].split()

    # we only care about the first arg, which has the die
    die = args[0]
    die_max = die[2:]

    # ensure the die is a positive integer
    if not die_max.isdigit():
        room.send_text('{} is not a positive number!'.format(die_max))
        return

    # and ensure it's a reasonable size, to prevent bot abuse
    die_max = int(die_max)
    if die_max <= 1 or die_max >= 1000:
        room.send_text('dice must be between 1 and 1000!')
        return

    # finally, send the result back
    result = random.randrange(1,die_max+1)
    room.send_text(str(result))


def main():
    # Create an instance of the MatrixBotAPI
    bot = MatrixBotAPI(USERNAME, PASSWORD, SERVER)
	
       # Add a regex handler waiting for the words from a list defined in global up top
    for index,item in enumerate(adios):								#loop through the word selection for index and item - may need to be 
        							
        hi_handler = MRegexHandler(item, hi_callback)
        bot.add_handler(hi_handler)
		  
    # Add a regex handler waiting for the echo command
    echo_handler = MCommandHandler("echo", echo_callback)
    bot.add_handler(echo_handler)

    # Add a regex handler waiting for the die roll command
    dieroll_handler = MCommandHandler("d", dieroll_callback)
    bot.add_handler(dieroll_handler)

    # Start polling
    bot.start_polling()

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        input()
        msg = in_common.get_input()   #doesnt work currently
        if msg == "/quit":
            break
        else:
            room.send_text(msg)


if __name__ == "__main__":
    main()
