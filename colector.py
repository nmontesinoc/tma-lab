import time
import netflow
import socket

def int_to_ip(ip):
    byte_4 = int((ip/256**3)%256) 
    byte_3 = int((ip/256**2)%256) 
    byte_2 = int((ip/256**1)%256) 
    byte_1 = int((ip/256**0)%256) 
    return str(byte_4) + "."+ str(byte_3) + "." + str(byte_2)  +"." + str(byte_1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 2055))

while True:
    try:
        payload, client = sock.recvfrom(4096)
        p = netflow.parse_packet(payload)
        for flow in p.flows:
            src_addr = int_to_ip(flow.IPV4_SRC_ADDR)
            dst_addr = int_to_ip(flow.IPV4_DST_ADDR)
            print(src_addr, dst_addr)
    except socket.timeout:
        time.sleep(1)  # wait for a flow to become available
