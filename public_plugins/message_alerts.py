import asyncio
from datetime import datetime
from termcolor import colored, cprint
import elasticsearch
import traceback

target_file = open('alert_target.conf', 'r')
target_set = set()

for line in target_file:
    target_set.add(line.replace('\n', ''))

es = elasticsearch.Elasticsearch()

print("[Public Plugin] <message_alerts.py>: Send alerts to console and to an ElasticSearch instance.")


def setup_index():
    elastic = elasticsearch.Elasticsearch()
    try:
        mapping = {
            "discord_alert": {
                "properties": {
                    "author_id": {"type": "string"},
                    "alert": {"type": "string"},
                    "server": {"type": "string"},
                    "author": {"type": "string", "index": "not_analyzed"},
                    "channel": {"type": "string", "index": "not_analyzed"},
                    "content": {"type": "string"},
                    "timestamp": {"type": "date"},
                }
            }
        }

        elastic.indices.create("discord_alerts")
        elastic.indices.put_mapping(index="discord_alerts", doc_type="discord_alert", body=mapping)

    except:
        traceback.print_exc()


@asyncio.coroutine
def action(message, client, config):
    time = datetime.now()

    for word in target_set:
        if word in message.content:
            alert_tag = colored("[Alert Text]", 'white', 'on_red', attrs=['bold'])
            alert_text = "[" + str(time) + "] <" + str(message.author) + "> : " + message.content
            print(alert_tag + " " + alert_text)

            alert_message = "wordlist"
            author = str(message.author)
            content = message.content
            server = str(message.server)
            channel = str(message.channel)
            timestamp = datetime.utcnow()
            author_id = str(message.author.id)

            body = {"alert": alert_message, "author_id": author_id, "server": server, "author": author,
                    "channel": channel, "content": content, "timestamp": timestamp}

            es.index(index='discord_alerts', doc_type='alert', body=body)

            # prevent alerting multiple times from one line
            break
