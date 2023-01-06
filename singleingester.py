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
def insert_row(ts,te,td,sa,da,sp,dp,pr,flg,fwd,stos,ipkt,ibyt,opkt,obyt,in2,out,sas,das,smk,dmk,dtos,dir2,nh,nhb,svln,dvln,ismc,odmc,idmc,osmc,mpls1,mpls2,mpls3,mpls4,mpls5,mpls6,mpls7,mpls8,mpls9,mpls10,cl,sl,al,ra,eng,exid,tr,Application,subapp):
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
                "fwd":int(fwd),
                "stos":int(stos),
                "ipkt":int(ipkt),
                "ibyt":int(ipkt),
                "opkt":int(opkt),
                "obyt":int(obyt),
                "in":int(in2),
                "out":int(out),
                "sas":int(sas),
                "das":int(das),
                "smk":int(smk),
                "dmk":int(dmk),
                "dtos":int(dtos),
                "dir":dir2,
                "nh":nh,
                "nhb":nhb,
                "svln":int(svln),
                "dvln":dvln,
                "ismc":ismc,
                "odmc":odmc,
                "idmc":idmc,
                "osmc":osmc,
                "mpls1":mpls1,
                "mpls2":mpls2,
                "mpls3":mpls3,
                "mpls4":mpls4,
                "mpls5":mpls5,
                "mpls6":mpls6,
                "mpls7":mpls7,
                "mpls8":mpls8,
                "mpls9":mpls9,
                "mpls10":mpls10,
                "cl":cl,
                "sl":int(sl),
                "al":int(al),
                "ra":ra,
                "eng":eng,
                "exid":int(exid),
                "tr":datetime.strptime("2023-1-1 00:"+tr, '%Y-%m-%d %H:%M:%S.%f'),
                "Application":Application,
                "Sub/App":subapp
                })
        
        


    
insert_row("16/10/2022 21:32","16/10/2022 21:32",0.022,"10.0.2.15","152.199.21.141",36402,443,"TCP",".....RS.",0,0,2,100,0,0,0,0,0,0,0,0,0,0,"0.0.0.0","0.0.0.0",0,0,"00:00:00:00:00:00","00:00:00:00:00:00","00:00:00:00:00:00","00:00:00:00:00:00","0-0-0","0-0-0","0-0-0","0-0-0","0-0-0","0-0-0","0-0-0","0-0-0","0-0-0","0-0-0",0,0,0,"127.0.0.1","0/0",1,"35:01.1","Twitter","Edge/CDN")    
result = es.count(index=index_name)
print(result.body['count'])



    


