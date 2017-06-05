from steam import webapi
import configparser

config = configparser.RawConfigParser()
config.read("config.conf")

api_key = config.get("Steam", "api")

# Setup Steam API
api = webapi.WebAPI(api_key)


def build_app_lookup():
    app_list = api.ISteamApps.GetAppList()['applist']['apps']
    app_dict = {}

    for app in app_list:
        app_dict[app['appid']] = app['name']

    return app_dict


def get_user_apps(steam_id):
    app_list = api.IPlayerService.GetOwnedGames(steamid=steam_id, include_played_free_games=False,
                                                include_appinfo=False, appids_filter="")['response']['games']

    recent_games = {}
    all_games = {}

    for app in app_list:

        # Check if game was played in the last 2 weeks
        if 'playtime_2weeks' in app.keys():
            recent_games[app['appid']] = app['playtime_2weeks']

        # Add every game to all_games
        all_games[app['appid']] = app['playtime_forever']

    return recent_games, all_games


def get_steam_id(profile_url):
    pass
