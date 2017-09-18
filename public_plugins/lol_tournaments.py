# TODO: Complete tournament workflow:
# TODO: tournament_start, tournament_join, tournament_end, game_start, game_join, game_end, game_stats
# TODO: Use reactions rather than chat commands to join the game
import asyncio
from libs.custom_games.libs.tournament_libs import TournamentManager
from libs import permissions

print("[Public Plugin] <lol_tournaments.py>: This plugin manages LoL custom tournaments.")

help_message = """
__**!tournament help** (Public Channels Only)__
Manages LoL Custom Tournaments

!season start <SEASON_NAME> - start a new season [requires permission]
!season end - end a season [requires permission]
!season get - get season details [requires permission]
"""

manager = TournamentManager()


def start_tournament(name):
    started = manager.start_tournament(name)
    return started


def tournament_end():
    tournament = manager.get_active_tournaments()[0]
    ended = tournament.complete_tournament()
    return ended


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()

    if split_content[0] == "!tournament":

        # Season management - Admin Only
        if (permissions.has_admin(message.author)) is not None:
            if len(split_content) == 3:
                if split_content[1] == "start":
                    name = split_content[2]
                    started = start_tournament(name)
                    if started:
                        start_message = f'Started {name} Tournament successfully.'
                        yield from client.send_message(message.channel, start_message)
                    else:
                        fail_message = "Tournament failed to start, there may already be one running."
                        yield from client.send_message(message.channel, fail_message)
            if split_content[1] == "end":
                stopped = tournament_end()

                if stopped:
                    start_message = f'Ended Tournament successfully.'
                    yield from client.send_message(message.channel, start_message)
                else:
                    fail_message = "Tournament failed to end."
                    yield from client.send_message(message.channel, fail_message)

            if split_content[1] == "list":
                tournament = manager.get_active_tournaments()[0]
                tourney_message = f"The current active tournament is {tournament.name}."
                yield from client.send_message(message.channel, tourney_message)

    if split_content[0] == "!game":
        # Game management - All Users
        if split_content[1] == "join":
            yield from client.send_message(message.channel, "JOIN")
