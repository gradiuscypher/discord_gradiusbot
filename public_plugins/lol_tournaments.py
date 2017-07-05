# TODO: Complete tournament workflow:
# TODO: tournament_start, tournament_join, tournament_end, game_start, game_join, game_end, game_stats
import asyncio

print("[Public Plugin] <lol_tournaments.py>: This plugin manages LoL custom tournaments.")

help_message = """
__**!tournament help** (Public Channels Only)__
Manages LoL Custom Tournaments

!tournament seasonstart - start a new season [requires permission]
!tournament join season - join the current season
!tournament join game - join the current game being created
!tournament stats - show the stats and leaderboard.
"""


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()

    if split_content[0] == "!tournament":
        if split_content[1] == "seasonstart":
            pass
        if split_content[1] == "join":
            if split_content[2] == "season":
                pass
            if split_content[2] == "game":
                pass
        if split_content[1] == "stats":
            pass
