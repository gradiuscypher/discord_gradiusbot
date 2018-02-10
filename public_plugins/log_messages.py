"""
Config Values:
[LogMessages]
# The elasticsearch host
elastic_host =
"""

import asyncio
import configparser
import traceback
import elasticsearch
from datetime import datetime
from sys import argv

# Plugin version
plugin_version = '1.0.0'

config = configparser.RawConfigParser()
config.read(argv[1])
elastic_host = config.get("LogMessages", "elastic_host")

es = elasticsearch.Elasticsearch([elastic_host])

print("[Public Plugin] <log_messages.py:{}>: Log messages to ElasticSearch.".format(plugin_version))


def setup_index():
    elastic = elasticsearch.Elasticsearch()
    try:
        mapping = {
            "chat_message": {
                "properties": {
                    "server": {"type": "string"},
                    "author": {"type": "string", "index": "not_analyzed"},
                    "channel": {"type": "string", "index": "not_analyzed"},
                    "content": {"type": "string"},
                    "timestamp": {"type": "date"},
                    "author_id": {"type": "string"},
                }
            }
        }

        elastic.indices.create("discord_chat")
        elastic.indices.put_mapping(index="discord_chat", doc_type="chat_message", body=mapping)

    except:
        traceback.print_exc()


@asyncio.coroutine
async def action(message, client, config):
    try:
        author = str(message.author)
        content = message.clean_content
        server = str(message.server)
        channel = str(message.channel)
        timestamp = datetime.utcnow()
        author_id = str(message.author.id)

        body = {"author_id": author_id, "server": server, "author": author, "channel": channel, "content": content,
                "timestamp": timestamp}

        es.index(index='discord_chat', doc_type='chat_message', body=body)

    except:
        traceback.print_exc()
