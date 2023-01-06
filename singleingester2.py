from elasticsearch import Elasticsearch,helpers
from datetime import datetime
from elasticsearchconfigurations2 import configurations
import csv, sys
import dateutil.parser
import os 
from datetime import datetime


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
def insert_row(ts,te,td,sa,da,sp,dp,pr,flg,ipkt,ibyt,tr,Application):
        es.index(
               
                index=index_name,
                document = {
                "ts":datetime.strptime(ts, '%d/%m/%Y %H:%M'),
                "te":datetime.strptime(te, '%d/%m/%Y %H:%M'),
                "td":float(td),
                "sa":sa,
                "da":da,
                "sp":int(sp),
                "dp":int(dp),
                "pr":pr,
                "flg":flg,
                "ipkt":int(ipkt),
                "ibyt":int(ipkt),
                "tr":'2023-01-01T00:'+tr+'Z',
                "Application":Application,
                })
        
        


    
insert_row("16/10/2022 21:32","16/10/2022 21:32",0.022,"10.0.2.15","152.199.21.141",36402,443,"TCP",".....RS.",2,100,"35:01.1","Twitter")    
result = es.count(index=index_name)
print(result.body['count'])



    


