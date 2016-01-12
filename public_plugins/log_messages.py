import asyncio
from datetime import datetime
import traceback
import elasticsearch

es = elasticsearch.Elasticsearch()

print("[Public Plugin] <log_messages.py>: Log messages to ElasticSearch.")


def setup_index():
    elastic = elasticsearch.Elasticsearch()
    try:
        mapping = {
            "chat_message": {
                "properties": {
                    "message_id": {"type": "string"},
                    "server": {"type": "string"},
                    "author": {"type": "string", "index": "not_analyzed"},
                    "channel": {"type": "string"},
                    "content": {"type": "string"},
                    "timestamp": {"type": "date"},
                }
            }
        }

        elastic.indices.create("discord_chat")
        elastic.indices.put_mapping(index="discord_chat", doc_type="chat_message", body=mapping)

    except:
        traceback.print_exc()


@asyncio.coroutine
def action(message, client):
    try:
        author = str(message.author)
        content = message.clean_content
        server = str(message.server)
        channel = str(message.channel)
        message_id = str(message.id)
        timestamp = datetime.utcnow()

        body = {"message_id": message_id, "server": server, "author": author, "channel": channel, "content": content,
                "timestamp": timestamp}

        es.index(index='discord_chat', doc_type='chat_message', body=body)

    except:
        traceback.print_exc()
