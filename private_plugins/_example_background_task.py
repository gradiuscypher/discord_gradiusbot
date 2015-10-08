from time import sleep


def action(message, send_message_callback):
    if message.content == "background":
        while True:
            send_message_callback(message.channel, "This will keep happening.")
            sleep(5)
