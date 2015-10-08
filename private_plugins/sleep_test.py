import time


def action(message, send_message_callback):
    message_split = message.content.split()

    if len(message_split) == 2 and message_split[0] == "sleep":
        send_message_callback(message.channel, "Sleeping: " + message.content)
        time.sleep(5)
        send_message_callback(message.channel, "Done sleeping: " + message.content)
