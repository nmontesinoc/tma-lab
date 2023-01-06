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
            
            "fwd": {"type":"integer"},
            "sto": {
                "type": "integer"},
            "ipkt": {"type":"integer"},
            "ibyte": {"type":"integer"},
            "opkt": {"type":"integer"},
            "obyte": {"type":"integer"},
            "in": {"type":"integer"},
            "out":{"type":"integer"},
            "sas":{"type": "integer"},
            "das": {"type":"integer"},
            "smk":{"type":"integer"},
            "dmk":{"type":"integer"},
            "dtos":{"type":"integer"},
            "dir":{"type":"integer"},
            "nh":{"type":"ip","index":"true","null_value":"0.0.0.0"},
            "nhb":{"type":"ip","index":"true","null_value":"0.0.0.0"},
            "svln":{"type":"integer"},
            "dvln":{"type":"keyword"},
            "ismc":{"type":"keyword"},
            "odmc":{"type":"keyword"},
            "mpls1":{"type":"keyword"},
            "mpls2":{"type":"keyword"},
            "mpls3":{"type":"keyword"},
            "mpls4":{"type":"keyword"},
            "mpls5":{"type":"keyword"},
            "mpls6":{"type":"keyword"},
            "mpls7":{"type":"keyword"},
            "mpls8":{"type":"keyword"},
            "mpls9":{"type":"keyword"},
            "mpls10":{"type":"keyword"},
            "cl":{"type":"keyword"},
            "sl":{"type":"integer"},
            "al":{"type":"integer"},
            "ra":{"type":"ip","index":"true","null_value":"0.0.0.0"},
            "eng":{"type":"keyword"},
            "exid":{"type":"keyword"},
            "tr":{"type":"date","format":"yyyy-MM-dd'T'HH:mm:ss.SSSZ||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            "Application":{"type":"keyword"},
            "Sub/App":{"type":"keyword"},
                }
            }
}
