from elasticsearch import Elasticsearch,helpers
from datetime import datetime
from elasticsearchconfigurations import configurations,configurations2
import csv, sys
import dateutil.parser
import os 
from datetime import datetime
def get_client():
   es = Elasticsearch(["http://34.175.204.146:9200"], basic_auth=('elastic', 'SUj3YT=QADBDug5c2QR*'))
   return es

def create_index(es):    
    #es = Elasticsearch(["http://34.175.204.146:9200"], basic_auth=('elastic', 'SUj3YT=QADBDug5c2QR*'))
    print(es.cluster.health())
    es.indices.create(

        index="flows",
        settings=configurations["settings"],
        mappings=configurations["mappings"],
        )
    es.indices.create(

        index="taggedflows",
        settings=configurations2["settings"],
        mappings=configurations2["mappings"],
        )

header = ["ts","te","td","sa","da","sp","dp","pr","flg","fwd","stos","ipkt","ibyt","opkt","obyt","in","out","sas","das","smk","dmk","dtos","dir","nh","nhb","svln","dvln","ismc","odmc","idmc","osmc","mpls1","mpls2","mpls3","mpls4","mpls5","mpls6","mpls7","mpls8","mpls9","mpls10","cl","sl","al","ra","eng","exid","tr","Application","Sub/App"]
def insert_row(es,ts,te,td,sa,da,sp,dp,pr,flg,ipkt,ibyt,tr):
   # es = Elasticsearch(["http://34.175.204.146:9200"], basic_auth=('elastic', 'SUj3YT=QADBDug5c2QR*'))
    print(es.cluster.health())
   
    index_name = "flows"
    es.index(
               
                index=index_name,
                document = {
                "ts":datetime.strptime(ts, '%Y-%m-%d %H:%M:%S'),
                "te":datetime.strptime(te, '%Y-%m-%d %H:%M:%S'),
                "td":float(td),
                "sa":sa,
                "da":da,
                "sp":int(sp),
                "dp":int(dp),
                "pr":pr,
                "flg":flg,
                "ipkt":int(ipkt),
                "ibyt":int(ibyt),
                "tr":tr
                })
        
        

def insert_classified_row(es,App,localip,datetime):
    print(es.cluster.health())
    index_name="taggedflows"
    es.index(
            index=index_name,
            document = {
                "Application":App,
                "local_ip":localip,
                "datetime":datetime
                })

    
index_name = "flows"
#insert_row("16/10/2022 21:32","16/10/2022 21:32",0.022,"10.0.2.15","152.199.21.141",36402,443,"TCP",".....RS.",2,100,"35:01.1","Twitter")    
#result = es.count(index=index_name)
#print(result.body['count'])