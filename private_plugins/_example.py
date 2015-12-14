def action(message, client):
    print("This is a private message")
    print("This is the sender:", message.author)
    print("This is the message:", message.content)
    client.send_message(message.channel, "Your message: " + message.content)
