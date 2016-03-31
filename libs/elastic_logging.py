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
                        "error_message": {"type": "string", "index": "not_analyzed"},
                        "author_message": {"type": "string", "index": "not_analyzed"},
                        "traceback": {"type": "string", "index": "not_analyzed"},
                        "app": {"type": "string"},
                        "error_type": {"type": "string"},
                        "extra_data": {"type": "string"},
                        "author_id": {"type": "string"},
                        "timestamp": {"type": "date"}
                    }
                }
            }

            elastic.indices.create("elastic_logs")
            elastic.indices.put_mapping(index="elastic_logs", doc_type="elastic_logger", body=mapping)

        except:
            traceback.print_exc()

    def log_message(self, server, channel, author, author_id, error_message, author_message, traceback, app, error_type, timestamp, extra_data):
        try:
            body = {"server": server, "channel": channel, "author": author, "error_message": error_message,
                    "traceback": traceback, "app": app, "error_type": error_type, "author_id": author_id,
                    "timestamp": timestamp}
            es.index(index='elastic_logs', doc_type='elastic_logger', body=body)
        except:
            traceback.print_exc()
