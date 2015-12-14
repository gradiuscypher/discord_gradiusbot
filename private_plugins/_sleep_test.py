import time


def action(message, client):
    message_split = message.content.split()

    if len(message_split) == 2 and message_split[0] == "sleep":
        client.send_message(message.channel, "Sleeping: " + message.content)
        time.sleep(5)
        client.send_message(message.channel, "Done sleeping: " + message.content)
