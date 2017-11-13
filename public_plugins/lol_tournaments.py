# TODO: Complete tournament workflow:
# TODO: tournament_start, tournament_join, tournament_end, game_start, game_join, game_end, game_stats
# TODO: Use reactions rather than chat commands to join the game
import asyncio
import discord.utils
from lol_customs.tournament_libs import TournamentManager
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


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()
    announce_channel_str = config.get("Tournament", "announce_channel")
    announce_channel = discord.utils.get(message.server.channels, name=announce_channel_str)

    if split_content[0] == "!season":

        # Season management - Admin Only
        if (permissions.has_admin(message.author)) is not None:
            if len(split_content) == 3:
                if split_content[1] == "start":
                    name = split_content[2]
                    started = manager.start_tournament(name)
                    if started:
                        start_message = 'Started {} Tournament successfully.'.format(name)
                        yield from client.send_message(message.channel, start_message)

                        if announce_channel is not None:
                            announce_message = '@here: {} has opened a new Customs season: [{}]'.format(message.author.name, name)
                            yield from client.send_message(announce_channel, announce_message)
                    else:
                        fail_message = "Tournament failed to start, there may already be one running."
                        yield from client.send_message(message.channel, fail_message)

            if split_content[1] == "end":
                active_tournaments = manager.get_active_tournaments()

                if len(active_tournaments) > 0:
                    stopped = active_tournaments[0].complete_tournament()

                    if stopped:
                        start_message = 'Ended Tournament successfully.'
                        yield from client.send_message(message.channel, start_message)

                        if announce_channel is not None:
                            announce_message = '@here: {} has closed the current Customs season.'.format(message.author.name)
                            yield from client.send_message(announce_channel, announce_message)
                    else:
                        fail_message = "Tournament failed to end."
                        yield from client.send_message(message.channel, fail_message)

            if split_content[1] == "list":
                tournaments = manager.get_active_tournaments()

                if len(tournaments) > 0:
                    tournament = tournaments[0]
                    tourney_message = "The current active tournament is {}.".format(tournament.name)
                    yield from client.send_message(message.channel, tourney_message)
                else:
                    tourney_message = 'There are no active tournaments.'
                    yield from client.send_message(message.channel, tourney_message)
