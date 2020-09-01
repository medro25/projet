from elasticsearch.client import Elasticsearch
from elasticsearch import helpers

indexName = "morocco-99"
print("Index Name: ", indexName)

es = Elasticsearch(hosts="http://localhost:9200")

results = es.search(body={
        "_source": "html",
        "size": 100,        
        "query": {
            "bool": {
                "must_not": {
                    "exists": {
                        "field": "processedText"
                    }            
                }
            }
        }
    }, index=indexName)

if len(results['hits']['hits']) > 0:
    print("Records Found: ", len(results['hits']['hits']) , "Processing Now")
    import re
    from bs4 import BeautifulSoup
    for item in range(len(results['hits']['hits'])):
        print("Processing", results['hits']['hits'][item]['_id'])
        soup = BeautifulSoup(results['hits']['hits'][item]['_source']['html'], 'html.parser')
        for script in soup(["script", "style",""]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        body = {
            "doc": {
                "processedText": text
            }
        }
        _update = es.update(index=results['hits']['hits'][item]['_index'], id=results['hits']['hits'][item]['_id'], body=body)
        print("HTML Cleaned, and Converted to Searchable Text, Updating Doc", _update)
        
print("Quiting Now")