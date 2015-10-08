def action(message, send_message_callback):
    print("This is a private message")
    print("This is the sender:", message.author)
    print("This is the message:", message.content)
    send_message_callback(message.channel, "I've seen your message privately: " + message.content)
