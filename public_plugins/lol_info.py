import asyncio
import configparser
import traceback
import random
from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError

print("[Public Plugin] <lol_info.py>: This plugin gives you LoL information.")

config = configparser.RawConfigParser()
config.read('config.conf')

api_key = config.get("BotSettings", "lol_api")

riotapi.set_region("NA")
riotapi.set_api_key(api_key)


@asyncio.coroutine
def action(message, client):
    split_message = message.content.split()

    if split_message[0] == "!lol":
        if split_message[1] == "last":
            try:
                summoner_name = ' '.join(split_message[2:])
                summoner = riotapi.get_summoner_by_name(summoner_name)
                last_game = summoner.recent_games()[0]

                champion = last_game.champion.name
                kda = last_game.stats.kda
                kda_tuple = (last_game.stats.kills, last_game.stats.deaths, last_game.stats.assists)
                cs = last_game.stats.minion_kills
                level = last_game.stats.level
                win = last_game.stats.win
                wards = last_game.stats.wards_placed
                vision_wards = last_game.stats.vision_wards_bought
                time_played = last_game.stats.time_played/60
                side = last_game.stats.side.name
                gold_earned = last_game.stats.gold_earned
                total_wards = wards + vision_wards

                role = last_game.stats.role
                if role is None:
                    role = "IDONTKNOW"
                else:
                    role = role.name

                lane = last_game.stats.lane
                if lane is None:
                    lane = "IDONTKNOW"
                else:
                    lane = lane.value.lower()

                if win:
                    victory = "won"
                else:
                    victory = "lost"

                message1 = "%s %s their last game as %s playing %s in the %s lane on the %s side in %.1f minutes." % (summoner_name, victory, champion, role, lane, side, time_played)
                message2 = "They finished the game with a KDA of %.1f and CS of %s. They were level %s and earned %s gold. They placed %s wards." % (kda, cs, level, gold_earned, total_wards)

                full_message = message1 + " " + message2

                yield from client.send_message(message.channel, full_message)
            except APIError as error:
                if error.error_code in [500]:
                    yield from client.send_message(message.channel, "I had trouble connecting, try again in a little while.")
                if error.error_code in [404]:
                    yield from client.send_message(message.channel, "I couldn't find that Summoner.")
            except:
                print(traceback.format_exc())

        if split_message[1] == "tip":
            try:
                tip_type = random.choice(['ally', 'enemy'])
                random_champ = random.choice(riotapi.get_champions())

                tip = "I ain't got no tips for you, soz."

                if tip_type == "ally":
                    tip = random.choice(random_champ.ally_tips)
                if tip_type == "enemy":
                    tip = random.choice(random_champ.enemy_tips)

                yield from client.send_message(message.channel, tip)
            except APIError as error:
                if error.error_code in [500]:
                    yield from client.send_message(message.channel, "I had trouble connecting, try again in a little while.")
            except:
                print(traceback.format_exc())
