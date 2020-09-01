from markupsafe import escape
from elasticsearch.client import Elasticsearch

from flask import Flask
app = Flask(__name__)


es = Elasticsearch(hosts="http://localhost:9200")
indexName="crime-*"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/search/<query>')
def query(query):
    results = es.search(body={
        "_source": "text",
        "size": 10,        
        "query": {
            "match": {
                "processedText": escape(query)
            }
        },
        "highlight": {
            "fields": {
                "processedText": {
                    "pre_tags" : ["<b>"], "post_tags" : ["</b>"]
                }
            }
        }
        }, index=indexName)
    return 'Query: %s' % results