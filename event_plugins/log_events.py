import asyncio
from datetime import datetime
import traceback
import elasticsearch

es = elasticsearch.Elasticsearch()

print("[Public Plugin] <log_events.py>: Log events to ElasticSearch.")


def setup_index():
    elastic = elasticsearch.Elasticsearch()
    try:
        mapping = {
            "discord_event": {
                "properties": {
                    "server": {"type": "string"},
                    "author": {"type": "string", "index": "not_analyzed"},
                    "author_id": {"type": "string"},
                    "channel": {"type": "string", "index": "not_analyzed"},
                    "content": {"type": "string"},
                    "timestamp": {"type": "date"},
                    "event_type": {"type": "string"},
                    "event_message": {"type": "string"},
                }
            }
        }

        elastic.indices.create("discord_events")
        elastic.indices.put_mapping(index="discord_events", doc_type="discord_event", body=mapping)

    except:
        traceback.print_exc()


@asyncio.coroutine
def action(object_before, client, config, event_type, object_after=None):
    server = str(object_before.server)
    timestamp = datetime.utcnow()
    event_message = None
    body = None

    if event_type == "delete" or event_type == "edit":
        author = str(object_before.author)
        channel = str(object_before.channel)
        content = object_before.content
        author_id = str(object_before.author.id)
        bot_channel = config.get("BotSettings", "bot_channel")

        if event_type == "delete" and channel != bot_channel:
            body = {"event_type": event_type, "server": server, "author": author, "event_message": event_message,
                    "channel": channel, "content": content, "timestamp": timestamp, "author_id": author_id}

        if (event_type == "edit") and (content != object_after.content):
            event_message = object_after.content
            body = {"event_type": event_type, "server": server, "author": author, "event_message": event_message,
                    "channel": channel, "content": content, "timestamp": timestamp, "author_id": author_id}

    if event_type == "member_update":
        author = object_before.name
        author_id = object_before.id
        event_message = object_after.name
        content = "namechange"

        if object_before.name != object_after.name:
            body = {"event_type": event_type, "server": server, "author": author, "event_message": event_message,
                    "channel": None, "content": content, "timestamp": timestamp, "author_id": author_id}

    if body is not None:
        es.index(index='discord_events', doc_type='discord_event', body=body)
