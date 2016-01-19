# TODO: Add error checking and implement.

import asyncio
from libs import amplitude_lib

print("[Public Plugin] <amplitude_highscore.py>: This plugin helps track amplitude high scores via screenshot proof.")

alib = amplitude_lib.AmplitudeLib()


@asyncio.coroutine
def action(message, client):
    split_content = message.content.split()

    if split_content[0] == "!score":

        if split_content[1] == "board":
            print("Show the scoreboard")

        elif split_content[1] == "valid":
            print("Validate the score.")

        elif split_content[1] == "update":
            print("Update the score.")
