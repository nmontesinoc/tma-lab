import datetime
import csv
import sys
import re
import netflow
import socket
from ingester import create_index,insert_row,insert_classified_row,get_client
#for Doc2Vec model loading and inference
from gensim.models.doc2vec import Doc2Vec

FORMAT = "%Y-%m-%d %H:%M:%S"

IP_ADDRESSES = []

PATTERN = None

STARTING_TIME = datetime.datetime.now()

IP_PROTOCOLS = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
    58: "ICMPv6"
}

def parsedate(x):
    if not isinstance(x, datetime.datetime):
        x = datetime.datetime.strptime(x, FORMAT)
    return x

def tsdiff(x, y):
    return (parsedate(x) - parsedate(y)).total_seconds()

def tsadd(x, seconds):
    d = datetime.timedelta(seconds=seconds)
    nd = parsedate(x) + d
    return nd.strftime(FORMAT)

def int_to_ip(ip):
    byte_4 = int((ip/256**3)%256) 
    byte_3 = int((ip/256**2)%256) 
    byte_2 = int((ip/256**1)%256) 
    byte_1 = int((ip/256**0)%256) 
    return str(byte_4) + "."+ str(byte_3) + "." + str(byte_2)  +"." + str(byte_1)

def collect_30_packets():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 2055))
    # payload, client = sock.recvfrom(4096)  # experimental, tested with 1464 bytes

    flows_collect=[]
    raw_flows = []

    i = 0

    while i < 5:
        print(i)
        print("TUKA")
        try:
            payload, client = sock.recvfrom(4096)  # experimental, tested with 1464 bytes
            p = netflow.parse_packet(payload)  # Test result: <ExportPacket v5 with 30 records>
            for flow in p.flows:

                duration = (flow.LAST_SWITCHED / 1000) - (flow.FIRST_SWITCHED / 1000)

                start_time = flow.FIRST_SWITCHED // 1000
                end_time = flow.LAST_SWITCHED // 1000

                start_time_formatted = tsadd(STARTING_TIME, start_time)
                end_time_formatted = tsadd(STARTING_TIME, end_time)

                src_addr = int_to_ip(flow.IPV4_SRC_ADDR)
                dst_addr = int_to_ip(flow.IPV4_DST_ADDR)
                
                src_port = flow.SRC_PORT
                dst_port = flow.DST_PORT

                proto = flow.PROTO
                flags = flow.TCP_FLAGS

                packets = flow.IN_PACKETS
                bytess = flow.IN_OCTETS

                time_received = p.header.timestamp
                time_received = datetime.datetime.fromtimestamp(time_received)
                time_received = time_received.strftime(FORMAT)

                flow = [start_time, src_addr, dst_addr, src_port, dst_port, packets]
                raw_flaw = [start_time_formatted, end_time_formatted, duration, src_addr, dst_addr, src_port, dst_port, IP_PROTOCOLS.get(proto, 'UNKNOWN'), flags, packets, bytess, time_received]
                flows_collect.append(flow)
                raw_flows.append(raw_flaw)
        except Exception as e:
            print("ERROR", e)
        i += 1

    print(raw_flows)
    for flow in raw_flows:
        print(flow)

    return flows_collect, raw_flows

def match_ip_format(ip):
    # Replace X with a regex that matches any number from 0 to 255
    print(ip)
    print(PATTERN.match(ip) is not None)
    
    return PATTERN.match(ip) is not None

def is_in_ip_addresses(ip):
    # print(ip)
    if PATTERN is not None:
        return match_ip_format(ip)
    else:
        return ip in IP_ADDRESSES


def read_data(filename):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        X = []

        for row in reader:
            if row[0] == 'Summary':
                break
            X.append(row)
    X.sort(key=lambda x: x[0])
    return X


def by_time(filename, seconds):
    reader = read_data(filename)
    X = []
    aggregated = {}
    prev_dict = {}
    x = {}
    local_ip = ''

    for count, row in enumerate(reader):
        local_ip = row[3]
        remote_ip = row[4]

        if is_in_ip_addresses(row[4]):
            local_ip = row[4]
            remote_ip = row[3]
        
        if local_ip not in x:
            x[local_ip] = set()
            prev_dict[local_ip] = [row[0], 0]

        if local_ip not in aggregated:
            aggregated[local_ip] = []

        td = tsdiff(row[0], prev_dict[local_ip][0])
        if row[5] == "80" or row[6] == "80" or row[5] == "443" or row[6] == "443":
            if td < seconds:
                x[local_ip].add(remote_ip)
                prev_dict[local_ip][1] += int(row[11])
            else:
                X.append(x[local_ip])
                aggregated[local_ip].append((x[local_ip], prev_dict[local_ip][1]))
                x[local_ip] = {remote_ip}
                prev_dict[local_ip][1] = int(row[5])
            prev_dict[local_ip][0] = row[0]

    for local_ip in x:
        if len(x[local_ip]) > 0:
            X.append(x[local_ip])
    return X, aggregated

def by_time_from_collector(reader, seconds):
    reader.sort(key=lambda x: int(x[0]))
    print(reader)
    aggregated = {} # A dictionary of key: local_ip and value: a list of tuples (ip_addresses, aggregated_packets)
    X = []
    prev_dict = {} # local_ip: (tdiff, num_packets)
    x = {}
    local_ip = ''

    for count, row in enumerate(reader):
        local_ip = row[1]
        remote_ip = row[2]

        if is_in_ip_addresses(row[2]):
            local_ip = row[2]
            remote_ip = row[1]
        
        if local_ip not in x:
            x[local_ip] = set()
            prev_dict[local_ip] = [row[0], 0]

        if local_ip not in aggregated:
            aggregated[local_ip] = []

        td = row[0] - prev_dict[local_ip][0]
        if row[3] == 80 or row[4] == 80 or row[3] == 443 or row[4] == 443:
            print("TUKA")
            if td < seconds:
                x[local_ip].add(remote_ip)
                prev_dict[local_ip][1] += row[5]
            else:
                X.append(x[local_ip])
                aggregated[local_ip].append((x[local_ip], prev_dict[local_ip][1]))
                x[local_ip] = {remote_ip}
                prev_dict[local_ip][1] = row[5]
            prev_dict[local_ip][0] = row[0]

    for local_ip in x:
        if len(x[local_ip]) > 0:
            X.append(x[local_ip])
    return X, aggregated

def infer(model, session):
    v1 = model.infer_vector(session)
    return model.dv.most_similar([v1], topn = 7425)[0][0]

def main_without_file():
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <max_seconds_between_flow> <ip_addressess_of_PCs> \n\n" + 
             "<ip_addresses_of_PCs> can be an IP format or a list of addresses separated by space eg. 10.0.2.15 10.0.2.16 or 10.0.2.X \n" +
             "\n")
        sys.exit(1)

    seconds = int(sys.argv[1])

    if len(sys.argv) == 3:
        if(sys.argv[2].find("X") != -1):
            IP_FORMAT = sys.argv[2]
            format = re.escape(IP_FORMAT) 
            format = format.replace('X', r'[0-9]{1,3}')
            # Compile the regex and match it against the IP address
            global PATTERN
            PATTERN = re.compile(format)
        else:
            IP_ADDRESSES.append(sys.argv[2])
    else:
        for i in range(2, len(sys.argv)):
            IP_ADDRESSES.append(sys.argv[i])

    es = get_client()
    while(True): 
        print("Iteration started")
        data, raw_flows = collect_30_packets()
            
        res, aggregated = by_time_from_collector(data, seconds)
    
        cnt = 0
    
        model = Doc2Vec.load("model.doc2vec")
    
        classified = []
    
        for key, value in aggregated.items():
            for session in value:
                classified.append((infer(model, list(session[0])), key))
                print(list(session[0]))
                print(infer(model, list(session[0])))

        for flows in raw_flows:
            insert_row(es,flows[0],flows[1],flows[2],flows[3],flows[4],flows[5],flows[6],flows[7],flows[8],flows[9],flows[10],flows[11])
        for classified_row in classified:
            insert_classified_row(es,classified_row[0],classified_row[1],datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    # Here goes the injection to elk part
    # classified - a list of tuples (application, local_ip)
    # raw_flows - a list of tuples go to line 85 to see the format


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 main.py <filename> <max_seconds_between_flow> <ip_addressess_of_PCs> \n\n" + 
             "<ip_addresses_of_PCs> can be an IP format or a list of addresses separated by space eg. 10.0.2.15 10.0.2.16 or 10.0.2.X \n" +
             "\n")
        sys.exit(1)

    filename = sys.argv[1]
    seconds = int(sys.argv[2])

    if len(sys.argv) == 4:
        if(sys.argv[3].find("X") != -1):
            IP_FORMAT = sys.argv[3]
            format = re.escape(IP_FORMAT) 
            format = format.replace('X', r'[0-9]{1,3}')
            # Compile the regex and match it against the IP address
            global PATTERN
            PATTERN = re.compile(format)
        else:
            IP_ADDRESSES.append(sys.argv[3])
    else:
        for i in range(3, len(sys.argv)):
            IP_ADDRESSES.append(sys.argv[i])

    res, aggregated = by_time(filename, seconds)
    cnt = 0

    model = Doc2Vec.load("model.doc2vec")
    print(res)

    classified = []

    for key, value in aggregated.items():
        for session in value:
            classified.append( (infer(model, list(session[0])), key))
            print(list(session[0]))
            print(infer(model,list(session[0])))

    es = get_client()

    for flows in raw_flows:
        insert_row(es,flows[0],flows[1],flows[2],flows[3],flows[4],flows[5],flows[6],flows[7],flows[8],flows[9],flows[10],flows[11])
    for classified_row in classified:
        insert_classified_row(es,classified_row[0],classified_row[1],datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


    # Here goes the injection to elk part
    # classified - a list of tuples (application, local_ip)


if __name__ == '__main__':
    #main()
    main_without_file()
