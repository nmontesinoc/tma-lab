configurations = {
    "settings": {
        "index": {"number_of_replicas": 2},
        "analysis": {
            "filter": {
                "ngram_filter": {
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 15,
                },
            },
            "analyzer": {
                "ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "ngram_filter"],
                },
            },
        },
    },
    "mappings": {
        "properties": {
            "timestart": {"type": "date","format":"yyyy/MM/dd HH:mm||yyyy-MM-dd||epoch_millis "},
            "timeend": {"type":"date","format": "yyyy/MM/dd HH:mm||yyyy-MM-dd||epoch_millis"},
            
            "timeduration": {"type":"float"},
            "sourcedaddr": {"type":"ip","index":"true","null_value":"0.0.0.0"},
        
            "dstaddr": {"type":"ip","index":"true","null_value":"0.0.0.0"},
            "srcport": {"type":"integer"},
            "dstport": {"type":"integer"},
            "protocol": {"type":"keyword"},
            "flag": {"type":"keyword"},
            "ipkt": {"type":"integer"},
            "ibyte": {"type":"integer"},
            "tr":{"type":"date","format":"yyyy-MM-dd'T'HH:mm:ss.S'Z'||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis||mm:ss.SZ||date_optional_time"}
        
    
                }
            }
}

configurations2 = {
    "settings": {
        "index": {"number_of_replicas": 2},
        "analysis": {
            "filter": {
                "ngram_filter": {
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 15,
                },
            },
            "analyzer": {
                "ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "ngram_filter"],
                },
            },
        },
    },
    "mappings": {
        "properties": {

            
            "Application": {"type":"keyword"},
    
            "local_ip": {"type":"ip","index":"true","null_value":"0.0.0.0"}


                }
            }
}

