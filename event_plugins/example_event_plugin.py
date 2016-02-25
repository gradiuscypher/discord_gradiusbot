import asyncio

print("[Public Plugin] <echo.py>: This plugin echoes stuff to a public channel.")


@asyncio.coroutine
def action(message, client, config, event_type, object_after=None):

    if event_type == "delete":
        yield from client.send_message(message.channel, "Deleted: " + message.content)
    if event_type == "edit":
        yield from client.send_message(message.channel, "Edited:\n " + "- " + message.content +
                                       "\n+ " + object_after.content)
