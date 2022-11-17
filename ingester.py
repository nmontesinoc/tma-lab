from elasticsearch import Elasticsearch,  helpers
import csv, sys

es = Elasticsearch(["http://0.0.0.0:9200"], basic_auth=('elastic', 'changeme'))
print(es.cluster.health())
upload_list = []
# Load all csv data
with open('data2.csv', newline='') as csvfile:
    
    data_list = []
    csv_data = csv.reader(csvfile)
    for row in csv_data:
        data_list.append(row)

    # separate out the headers from the main data 
    headers = data_list[0]
    # drop headers from data_list
    data_list.pop(0)

    for item in data_list: # iterate over each row/item in the csv

        item_dict = {}

        # match a column header to the row data for an item
        i = 0
        for header in headers:
            item_dict[header] = item[i]
            i = i+1

        # add the transformed item/row to a list of dicts
        upload_list += [item_dict]

# using helper library's Bulk API to index list of Elasticsearch docs
try:
    resp = helpers.bulk(
        es,
        upload_list,
        index="flows"
    )
    msg = "helpers.bulk() RESPONSE: " + str(resp)
    print(msg) # print the response returned by Elasticsearch
except Exception as err:
    msg = "Elasticsearch helpers.bulk() ERROR: " + str(err)
    print(msg)
    sys.exit(1)

