import asyncio
import elasticsearch
import pprint
from elasticsearch.exceptions import NotFoundError

print("[Public Plugin] <albion_market.py>: This plugin provides Albion market information.")
es = elasticsearch.Elasticsearch("elastic1.lab.grds.io")


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()

    if split_content[0] == "!gold":
        # Query to see if gold timestamp is already in DB
        id_query = {
            "sort": [
                {"timestamp": "desc"}
            ],
            "query": {
                "bool": {
                    "must": [
                        {"range": {"timestamp": {"gte": "now-7d", "lte": "now"}}},
                        {"term": {"_type": "gold_price"}}
                    ]
                }
            }
        }
        try:
            result = es.search(index="albion_market", doc_type="gold_price", body=id_query)

            if len(result['hits']['hits']) > 0:
                first = result['hits']['hits'][0]['_source']
                gold = first['price']
                timestamp = first['timestamp'].replace("T", "")
                yield from client.send_message(message.channel,
                                               "The last recorded price for gold was `{}` at `{}` server time.".format(gold, timestamp))

        except NotFoundError as e:
            print("Index not found")
            print(e)
