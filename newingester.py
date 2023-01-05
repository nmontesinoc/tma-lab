from elasticsearch import Elasticsearch,  helpers
from elasticsearchindexconfigurations import configurations
import csv, sys


    
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
    with open("data2.csv", "r") as fi:

        reader = csv.DictReader(fi,delimiter=",",fieldnames = header)
        actions = []
        next(reader)
        next(reader)
    

        for row in reader:
            doc = {
                "_index": index_name,
                "_source":{
                    "ts":row["ts"],
                    "te":row["te"],
                    "td":row["td"],
                    "sa":row["sa"],
                    "da":row["da"],
                    "sp":row["sp"],
                    "dp":row["dp"],
                    "pr":row["pr"],
                    "flg":row["flg"],
                    "fwd":row["fwd"],
                    "stos":row["stos"],
                    "ipkt":row["ipkt"],
                    "ibyt":row["ipkt"],
                    "opkt":row["opkt"],
                    "obyt":row["obyt"],
                    "in":row["in"],
                    "out":row["out"],
                    "sas":row["sas"],
                    "das":row["das"],
                    "smk":row["smk"],
                    "dmk":row["dmk"],
                    "dtos":row["dtos"],
                    "dir":row["dir"],
                    "nh":row["nh"],
                    "nhb":row["nhb"],
                    "svln":row["svln"],
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
                    "sl":row["sl"],
                    "al":row["al"],
                    "ra":row["ra"],
                    "eng":row["eng"],
                    "exid":row["exid"],
                    "tr":row["tr"],
                    "Application":row["Application"],
                    "Sub/App":row["Sub/App"]
                },
        }
        yield doc 

helpers.bulk(es, generate_docs())
    
    
result = es.count(index=index_name)
print(result.body['count'])



    


