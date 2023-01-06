from elasticsearch import Elasticsearch,helpers
from datetime import datetime
from elasticsearchindexconfigurations import configurations
import csv, sys
import os 

os.system('head -n-3 data2.csv > data3.csv')    
es = Elasticsearch(["http://0.0.0.0:9200"])
print(es.cluster.health())
es.indices.create(
        index="flows",
        settings=configurations["settings"],
        mappings=configurations["mappings"],
        )
index_name = "flows"
header = ["ts","te","td","sa","da","sp","dp","pr","flg","fwd","stos","ipkt","ibyt","opkt","obyt","in","out","sas","das","smk","dmk","dtos","dir","nh","nhb","svln","dvln","ismc","odmc","idmc","osmc","mpls1","mpls2","mpls3","mpls4","mpls5","mpls6","mpls7","mpls8","mpls9","mpls10","cl","sl","al","ra","eng","exid","tr","Application","Sub/App"]
def generate_docs():
    with open("data3.csv", "r") as fi:

        reader = csv.DictReader(fi,delimiter=",",fieldnames = header)
        actions = []
        next(reader)
        next(reader)
    

        for row in reader:
            doc = {
                "_index": index_name,
                "_type":"document",
                "_source":{
                    "ts":datetime.strptime(row["ts"], '%d/%m/%Y %H:%M'),
                    "te":datetime.strptime(row["te"], '%d/%m/%Y %H:%M'),
                    "td":float(row["td"]),
                    "sa":row["sa"],
                    "da":row["da"],
                    "sp":int(row["sp"]),
                    "dp":int(row["dp"]),
                    "pr":row["pr"],
                    "flg":row["flg"],
                    "fwd":int(row["fwd"]),
                    "stos":int(row["stos"]),
                    "ipkt":int(row["ipkt"]),
                    "ibyt":int(row["ipkt"]),
                    "opkt":int(row["opkt"]),
                    "obyt":int(row["obyt"]),
                    "in":int(row["in"]),
                    "out":int(row["out"]),
                    "sas":int(row["sas"]),
                    "das":int(row["das"]),
                    "smk":int(row["smk"]),
                    "dmk":int(row["dmk"]),
                    "dtos":int(row["dtos"]),
                    "dir":row["dir"],
                    "nh":row["nh"],
                    "nhb":row["nhb"],
                    "svln":int(row["svln"]),
                    "dvln":row["dvln"],
                    "ismc":row["ismc"],
                    "odmc":row["odmc"],
                    "idmc":row["idmc"],
                    "osmc":row["osmc"],
                    "mpls1":row["mpls1"],
                    "mpls2":row["mpls2"],
                    "mpls3":row["mpls3"],
                    "mpls4":row["mpls4"],
                    "mpls5":row["mpls5"],
                    "mpls6":row["mpls6"],
                    "mpls7":row["mpls7"],
                    "mpls8":row["mpls8"],
                    "mpls9":row["mpls9"],
                    "mpls10":row["mpls10"],
                    "cl":row["cl"],
                    "sl":int(row["sl"]),
                    "al":int(row["al"]),
                    "ra":row["ra"],
                    "eng":row["eng"],
                    "exid":row["exid"],
                    "tr":datetime.strptime(row["tr"], '%M:%S.%f'),
                    "Application":row["Application"],
                    "Sub/App":row["Sub/App"]
                },
        }
        yield doc 

helpers.bulk(es, generate_docs())
    
    
result = es.count(index=index_name)
print(result.body['count'])



    


