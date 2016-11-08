import elasticsearch
import traceback

es = elasticsearch.Elasticsearch()


class ElasticLogging:

    def __init__(self):
        pass

    def setup_index(self):
        elastic = elasticsearch.Elasticsearch()
        try:
            mapping = {
                "elastic_logger": {
                    "properties": {
                        "server": {"type": "string", "index": "not_analyzed"},
                        "channel": {"type": "string", "index": "not_analyzed"},
                        "author": {"type": "string", "index": "not_analyzed"},
                        "message": {"type": "string", "index": "not_analyzed"},
                        "traceback": {"type": "string", "index": "not_analyzed"},
                        "app": {"type": "string"},
                        "error_type": {"type": "string"},
                        "extra_data": {"type": "string"},
                        "author_id": {"type": "string"},
                        "message_timestamp": {"type": "date"}
                    }
                }
            }

            elastic.indices.create("elastic_logs")
            elastic.indices.put_mapping(index="elastic_logs", doc_type="elastic_logger", body=mapping)

        except:
            traceback.print_exc()

    def log_message(self, message, trace_string, app, error_type, extra_data=""):
        try:
            if message.server is None:
                server = "private"
            else:
                server = message.server.name

            if message.channel is None:
                channel = "private"
            else:
                channel = message.channel.name

            author = message.author.name
            author_id = message.author.id
            message_content = message.content
            timestamp = message.timestamp

            body = {"server": server, "channel": channel, "author": author, "traceback": trace_string, "app": app,
                    "error_type": error_type, "author_id": author_id, "message_timestamp": timestamp,
                    "message": message_content, "extra_data": extra_data}
            es.index(index='elastic_logs', doc_type='elastic_logger', body=body)
        except:
            print(traceback.print_exc())
