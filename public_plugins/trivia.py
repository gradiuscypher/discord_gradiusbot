import asyncio
import time
from threading import Thread

print("[Public Plugin] <trivia.py>: Trivia plugin.")

global filling_teams
filling_teams = False
global trivia_game
trivia_game = False
global trivia_answer
trivia_answer = "taco"


@asyncio.coroutine
def action(message, client):

    global filling_teams
    global trivia_game
    global trivia_answer

    if message.content == "!triviastart":

        # Fill teams loop
        filling_teams = True
        invite_message = "A trivia game is staring!"
        yield from client.send_message(message.channel, invite_message)
        t = Thread(target=fill_teams)
        t.start()
        while t.is_alive():
            yield from client.send_message(message.channel, "You have 30 seconds to join! Type !triviajoin to be placed on a team!")
            yield from asyncio.sleep(5)
            yield from client.send_message(message.channel, "You have 15 seconds to join! Type !triviajoin to be placed on a team!")
            yield from asyncio.sleep(5)
            yield from client.send_message(message.channel, "The game is now starting!")
            filling_teams = False

        # Trivia game loop
        trivia_game = True
        # t_game_thread = Thread(target=trivia_loop)
        # t_game_thread.start()
        # while t_game_thread.is_alive():

    if filling_teams:
        if message.content == "!triviajoin":
            yield from client.send_message(message.channel, "I'll add you to a team, " + str(message.author) + ".")

    if trivia_game:
        if str(message.channel) == "testgradius":
            if message.content == trivia_answer:
                yield from client.send_message(message.channel, "That is correct, " + str(message.author) + "!")


def fill_teams():
    time.sleep(10)
