from elasticsearch import Elasticsearch,  helpers
import csv, json
import pandas as pd

es = Elasticsearch(["http://0.0.0.0:9200"], basic_auth=('elastic', 'changeme'))
print(es.cluster.health())
df = pd.read_csv("data2.csv")
json_str = df.to_json(orient='records')

json_records = json.loads(json_str)

index_name = 'flows'
doctype = 'flows_record'
es.indices.delete(index=index_name, ignore=[400, 404])
es.indices.create(index=index_name, ignore=400)
action_list = []
for row in json_records:
    record ={
        '_op_type': 'index',
        '_index': index_name,
        '_type' : doctype,
        '_source': row
    }
    action_list.append(record)
print(action_list)
