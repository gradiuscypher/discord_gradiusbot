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
def action(message, client, config, event_type, message_after=None):
    author = str(message.author)
    content = message.content
    server = str(message.server)
    channel = str(message.channel)
    timestamp = datetime.utcnow()
    author_id = str(message.author.id)
    event_message = None
    body = None

    if event_type == "delete":
        body = {"event_type": event_type, "server": server, "author": author, "event_message": event_message,
                "channel": channel, "content": content, "timestamp": timestamp, "author_id": author_id}

    if event_type == "edit":
        event_message = content + " > " + message_after.content
        body = {"event_type": event_type, "server": server, "author": author, "event_message": event_message,
                "channel": channel, "content": content, "timestamp": timestamp, "author_id": author_id}

    if body is not None:
        es.index(index='discord_events', doc_type='discord_event', body=body)

