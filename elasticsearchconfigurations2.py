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
            "ts": {"type": "date","format":"yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis "},
            "te": {"type":"date","format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            
            "td": {"type":"float"},
            "sa": {"type":"ip","index":"true","null_value":"0.0.0.0"},
        
            "da": {"type":"ip","index":"true","null_value":"0.0.0.0"},
            "sp": {"type":"integer"},
            "dp": {"type":"integer"},
            "pr": {"type":"keyword"},
            "flg": {"type":"keyword"},
            "ipkt": {"type":"integer"},
            "ibyt": {"type":"integer"},
            "tr":{"type":"date","format":"yy-MM-dd HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss.S'Z'||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis||mm:ss.SZ||date_optional_time"}
        
    
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
    
            "local_ip": {"type":"ip","index":"true","null_value":"0.0.0.0"},
            "datetime": {"type":"date","format":"dd/MM/yyyy HH:mm:ss"}


                }
            }
}

