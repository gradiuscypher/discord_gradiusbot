import asyncio
import discord
import traceback
import json
from discord import Embed, Color, utils
from lol_customs import tournament_libs

# TODO: Add debug strings that get sent to a chat channel - send message when doing any actions
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


def parse_eog_json(eog_json):
    game_json = json.loads(eog_json)
    summary_dict = {
        'teams': {
            100: {'players': '', 'win': False},
            200: {'players': '', 'win': False},
        },
        'winning_team': None,
        'summary_url': 'https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/{}?tab=overview'.format(
            game_json['gameId']
        ),
        'map_type': game_json['gameMode']
    }
    player_identities = {}

    # Build the teams list
    for player in game_json['participantIdentities']:
        player_identities[player['participantId']] = player['player']['summonerName']

    for player in game_json['participants']:
        if player['teamId'] == 100:
            summary_dict['teams'][100]['players'] += player_identities[player['participantId']] + "\n"
        if player['teamId'] == 200:
            summary_dict['teams'][200]['players'] += player_identities[player['participantId']] + "\n"

    # Get who won and build team dict
    teams = game_json['teams']
    for team in teams:
        if team['win'] == 'Win':
            summary_dict['teams'][team['teamId']]['win'] = True
            summary_dict['winning_team'] = team['teamId']
    return summary_dict


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
    announce_channel_name = config.get("Tournament", "announce_channel")
    announce_channel = None

    while True:
        if embed_channel is None:
            embed_channel = discord.utils.get(client.get_all_channels(), name=embed_channel_name)
        if announce_channel is None:
            announce_channel = discord.utils.get(client.get_all_channels(), name=announce_channel_name)

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
        if game_dict["SUMMONERS_RIFT"] is not None:
            new_sr_players = game_dict['SUMMONERS_RIFT'].get_players_in_lobby()
        if game_dict["HOWLING_ABYSS"] is not None:
            new_aram_players = game_dict['HOWLING_ABYSS'].get_players_in_lobby()

        if set(new_aram_players) != set(players_aram) and aram_embed is not None and embed_channel:
            # Update ARAM players
            new_aram_embed = build_embed("ARAM Custom", new_aram_players, game_dict["HOWLING_ABYSS"].tournament_code, Color.dark_blue())
            yield from client.purge_from(embed_channel, check=is_aram)
            yield from client.send_message(embed_channel, embed=new_aram_embed)
            aram_embed = new_aram_embed
            players_aram = new_aram_players

        if set(new_sr_players) != set(players_sr) and sr_embed is not None and embed_channel:
            # Update SR players
            new_sr_embed = build_embed("Summoner's Rift Custom", new_sr_players, game_dict["SUMMONERS_RIFT"].tournament_code, Color.dark_green())
            yield from client.purge_from(embed_channel, check=is_summoners)
            yield from client.send_message(embed_channel, embed=new_sr_embed)
            aram_embed = new_sr_embed
            players_sr = new_sr_players

        # Check to see if a game has started, if it has, alert the channel - get_lobby_status
        sr_start = game_dict["SUMMONERS_RIFT"].is_game_started()
        aram_start = game_dict["HOWLING_ABYSS"].is_game_started()

        if sr_start and announce_channel:
            yield from client.send_message(announce_channel, "A Summoner's Rift game has started!")
        if aram_start and announce_channel:
            yield from client.send_message(announce_channel, "An ARAM game has started!")

        # Check to see if a game has completed, if it has alert the channel
        if announce_channel:
            finished_games = tournament.check_for_finished_games()
            for game in finished_games:
                game_dict = parse_eog_json(game.eog_json)

                game_summary_embed = Embed(title='{} - Game Summary'.format(game_dict['map_type']), color=Color.gold())
                game_summary_embed.add_field(name='Match History URL', value=game_dict['summary_url'])

                for team_id in game_dict['teams'].keys():
                    if game_dict['teams'][team_id]['win']:
                        game_summary_embed.add_field(name='Victory', value=game_dict['teams'][team_id]['players'], inline=True)
                    else:
                        game_summary_embed.add_field(name='Defeat', value=game_dict['teams'][team_id]['players'], inline=True)
                yield from client.send_message(announce_channel, embed=game_summary_embed)

        # Sleep for the wait period before running these loops again
        yield from asyncio.sleep(5)
