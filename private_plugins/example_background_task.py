from time import sleep


def action(message, client):
    if message.content == "background":
        while True:
            client.send_message(message.channel, "This will keep happening.")
            sleep(5)
