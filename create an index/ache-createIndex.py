from elasticsearch import helpers
from elasticsearch.client import Elasticsearch

indexName = "morocco"

print("Index Name: ", indexName)

es = Elasticsearch(hosts="http://localhost:9200")

indexSettings ={
   "settings":{ 
      "index.number_of_replicas":0,
      "index.number_of_shards":1,
      "analysis":{
         "analyzer":{
            "autocomplete":{
               "type":"custom",
               "tokenizer":"standard",
               "filter":[
                  "lowercase",
                  "autocomplete_filter"
               ]
            },
            "analyzer_shingle":{
               "tokenizer":"standard",
               "filter":[
                  "apostrophe",
                  "filter_case_sensitive_stop_word",
                  "lowercase",
                  "filter_case_insensitive_stop_word",
                  "filter_shingle",
                  "trim",
                  "my_length"
               ]
            },
            "my_english_analyzer":{
               "tokenizer":"standard",
               "filter":[
                  "lowercase",
                  "apostrophe"
               ]
            },
            "lowerKeyword":{
               "type":"custom",
               "filter":[
                  "lowercase"
               ],
               "tokenizer":"keyword"
            }
         },
         "filter":{
            "autocomplete_filter":{
               "type":"edge_ngram",
               "min_gram":2,
               "max_gram":20,
               "token_chars":[
                  "letter",
                  "digit",
                  "whitespace",
                  "punctuation"
               ]
            },
            "filter_shingle":{
               "type":"shingle",
               "max_shingle_size":2,
               "min_shingle_size":2,
               "filler_token":"",
               "output_unigrams":"true"
            },
            "filter_case_insensitive_stop_word":{
               "type":"stop",
               "stopwords":[
                  "from",
                  "for",
                  "with",
                  "a",
                  "of",
                  "to",
                  "by",
                  "the",
                  "and",
                  "has",
                  "had",
                  "said",
                  "was",
                  "on",
                  "this",
                  "that",
                  "its",
                  "at",
                  "or",
                  "which",
                  "an",
                  "in",
                  "they",
                  "his",
                  "are",
                  "were",
                  "as",
                  "if",
                  "would",
                  "be"
               ]
            },
            "filter_case_sensitive_stop_word":{
               "type":"stop",
               "stopwords":[
                  "will",
                  "who",
                  "it",
                  "It",
                  "is"
               ]
            },
            "my_length":{
               "type":"length",
               "min":2
            }
         }
      }
   },
   "mappings":{
      "properties":{
         "crawlerId":{
            "type":"keyword"
         },
         "domain":{
            "type":"keyword"
         },
         "topPrivateDomain":{
            "type":"keyword"
         },
         "url":{
            "type":"text"
         },
         "html":{
            "enabled":"false"
         },
         "isRelevant":{
            "type":"keyword"
         },
         "relevance":{
            "type":"float"
         },
         "float":{
            "type":"keyword"
         },
         "retrieved":{
            "type":"date"
         },
         "title":{
            "type":"text",
            "analyzer":"autocomplete",
            "search_analyzer":"standard"
         },
         "text":{
            "type":"text",
            "analyzer":"analyzer_shingle",
            "search_analyzer":"standard"
         },
         "processedText":{
            "type":"text",
            "analyzer":"autocomplete",
            "search_analyzer":"standard"
         }
      }
   }
}

print("Checking if Index Exists")
if es.indices.exists(index=indexName):
    print("Found! Deleting Index", indexName)
    es.indices.delete(index=indexName)
    
print("Creating Index Now")
_res = es.indices.create(index=indexName, body=indexSettings)

print("{} Index Created & Shared Acknowledged {}".format(_res['index'], _res['shards_acknowledged']))