import asyncio
import discord
import traceback
from discord import Embed, Color, utils
from lol_customs import tournament_libs

print("[Scheduled Task] <custom_game_manager.py>: Helps manage and update custom games and their chat alerts.")

tm = tournament_libs.TournamentManager()

try:
    tournament = tm.get_active_tournaments()[0]
except:
    print("Unable to get an active tournament.")
    print(traceback.format_exc())


def is_embed(message):
    return len(message.embeds) > 0


def is_aram(message):
    if len(message.embeds) > 0:
        if message.embeds[0]['title'] == "ARAM Custom":
            return True
    return False


def is_summoners(message):
    if len(message.embeds) > 0:
        if message.embeds[0]['title'] == "Summoner's Rift Custom":
            return True
    return False


def build_embed(embed_target, players, tournament_code, color):
    target_embed = Embed(title=embed_target, color=color)

    if len(players) > 0:
        target_embed.add_field(name="Players", value='\n'.join(players), inline=True)
    else:
        target_embed.add_field(name="Players", value='Lobby is empty...', inline=True)

    target_embed.add_field(name="Ready Members", value=str(len(players))+"/10")
    target_embed.add_field(name="Tournament Code", value=tournament_code)
    return target_embed


@asyncio.coroutine
def action(client, config):
    # Game Embeds
    aram_embed = None
    sr_embed = None
    players_aram = []
    players_sr = []
    embed_channel_name = config.get("Tournament", "embed_channel")
    embed_channel = None

    while True:
        if embed_channel is None:
            embed_channel = discord.utils.get(client.get_all_channels(), name=embed_channel_name)

        # Get Open Games
        game_dict = {"SUMMONERS_RIFT": None, "HOWLING_ABYSS": None}
        for game in tournament.get_open_games():
            game_dict[game.map_name] = game

        # Check to see if there's an active game available for both maps, if not, start one
        # Set the embed objects to None to force an Embed refresh
        # If a Summoners Rift game doesn't exist
        if game_dict["SUMMONERS_RIFT"] is None:
            tournament.create_game("00000", "SUMMONERS_RIFT")
            sr_embed = None
        # If an ARAM game doesn't exist
        if game_dict["HOWLING_ABYSS"] is None:
            tournament.create_game("00000", "HOWLING_ABYSS")
            aram_embed = None

        # Check to see if sr_embed or aram_embed is None, if so, create new Embeds for both and delete the old ones
        if (aram_embed is None) or (sr_embed is None):

            if embed_channel:
                yield from client.purge_from(embed_channel, check=is_embed)

                # Get the current games to build both embeds
                if game_dict["HOWLING_ABYSS"] is not None:
                    aram_embed = build_embed("ARAM Custom", [], game_dict["HOWLING_ABYSS"].tournament_code, Color.dark_blue())
                    yield from client.send_message(embed_channel, embed=aram_embed)

                if game_dict["SUMMONERS_RIFT"] is not None:
                    sr_embed = build_embed("Summoner's Rift Custom", [], game_dict["SUMMONERS_RIFT"].tournament_code, Color.dark_green())
                    yield from client.send_message(embed_channel, embed=sr_embed)

        # Check to see if anyone's joined the active lobbies and update the Embeds
        new_sr_players = game_dict['SUMMONERS_RIFT'].get_players_in_lobby()
        new_aram_players = game_dict['HOWLING_ABYSS'].get_players_in_lobby()

        if set(new_aram_players) != set(players_aram) and aram_embed is not None:
            # Update ARAM players
            new_aram_embed = build_embed("ARAM Custom", new_aram_players, game_dict["HOWLING_ABYSS"].tournament_code, Color.dark_blue())
            yield from client.purge_from(embed_channel, check=is_aram)
            yield from client.send_message(embed_channel, embed=new_aram_embed)
            aram_embed = new_aram_embed
            players_aram = new_aram_players

        if set(new_sr_players) != set(players_sr) and sr_embed is not None:
            # Update SR players
            new_sr_embed = build_embed("Summoner's Rift Custom", new_sr_players, game_dict["SUMMONERS_RIFT"].tournament_code, Color.dark_green())
            yield from client.purge_from(embed_channel, check=is_summoners)
            yield from client.send_message(embed_channel, embed=new_sr_embed)
            aram_embed = new_sr_embed
            players_sr = new_sr_players

        # Check to see if a game has started, if it has, alert the channel - get_lobby_status
        # TODO: Complete game start notification message
        # TODO: Add debug strings that get sent to a chat channel - send message when doing any actions

        sr_start = game_dict["SUMMONERS_RIFT"].is_game_started()
        aram_start = game_dict["HOWLING_ABYSS"].is_game_started()

        if sr_start:
            print("SUMMONERS RIFT HAS STARTED!")
        if aram_start:
            print("ARAM HAS STARTED!")

        # TODO: To check finished games, you can't check the game in the list, you have to get the running but not finished game
        # Check to see if a game has completed, if it has alert the channel - check_game_status
        # sr_finished = game_dict["SUMMONERS_RIFT"].is_game_finished()
        # aram_finished = game_dict["HOWLING_ABYSS"].is_game_finished()
        #
        # if sr_finished:
        #     print("SUMMONERS RIFT HAS FINISHED!")
        # if aram_finished:
        #     print("ARAM HAS FINISHED!")

        # Sleep for the wait period before running these loops again
        yield from asyncio.sleep(5)
