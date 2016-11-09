import asyncio
from datetime import datetime
import traceback

#TODO: Finish this?


@asyncio.coroutine
def action(object_before, client, config, event_type, object_after=None):
    server = str(object_before.server)
    timestamp = datetime.utcnow()
    event_message = None
    body = None
    attachment = None

    if event_type == "delete":
        author = str(object_before.author)
        channel = str(object_before.channel)
        content = object_before.clean_content
        author_id = str(object_before.author.id)
        bot_channel = config.get("BotSettings", "bot_channel")
