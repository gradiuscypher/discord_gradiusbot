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

print("Message alerting enabled.")


# TODO: Alert on deleted messages
def setup_index():
    elastic = elasticsearch.Elasticsearch()
    try:
        mapping = {
            "discord_alert": {
                "properties": {
                    "alert": {"type": "string"},
                    "message_id": {"type": "string"},
                    "server": {"type": "string"},
                    "author": {"type": "string", "index": "not_analyzed"},
                    "channel": {"type": "string"},
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
def action(message, client):
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
            message_id = str(message.id)
            timestamp = datetime.utcnow()

            body = {"alert": alert_message, "message_id": message_id, "server": server, "author": author,
                    "channel": channel, "content": content, "timestamp": timestamp}

            es.index(index='discord_alerts', doc_type='alert', body=body)

            # prevent alerting multiple times from one line
            break
