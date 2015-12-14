import configparser


config = configparser.RawConfigParser()
config.read('config.conf')


def action(message, client):
    if message.channel.name == config.get('Settings', 'bot_channel'):
        client.delete_message(message)
