#!/usr/bin/env python

import socket
import struct
import sys
import re

# Monitor all Ethernet packets
# See <linux/if_ether.h>
ETH_P_ALL = 0x0003
# Monitor all IP packets only
# ETH_P_IP = 0x0800

# Source Mac: 6, Dst mac: 6, packet_type: 2
# See <linux/if_ether.h>
ETH_H_LEN = 14
# IP header length 
IP_H_LEN = 20
# TCP header length
TCP_H_LEN = 20 

method_str = '(GET|POST|HEAD|TRACE|CONNECT|PUT|DELETE|PATCH)'
path_str = '(\/.*)'
version_str = '(HTTP\/1\.[0-1])'

req_re = '%s %s %s' %(method_str, path_str, version_str)
host_re = "^Host:\s(.*)$"
useragent_re = "^User-Agent:\s(.*\/)$"

def parse_payload(payload):
    """
    Get the payload now
    Search for this pattern:
    HTTP methods: [GET, POST, HEAD, TRACE, CONNECT, PUT, DELETE, CONNECT, PATCH]
    """
    req = re.search(req_re, payload)
    host = re.search(host_re, payload)
    useragent = re.search(useragent_re, payload)

    try:
        method = req.group(1)
        path  = req.group(2)
        ver = req.group(3)
        host = host.group(1)
        useragent = useragent.group(1)
        print "Method: %s" %method
        print "Path: %s" %path
        print "Version: %s" %ver
        print "Host: %s" %host
        print "UA: %s" %useragent
    except:
        pass

def tcp_parse(local_ip, packet, ip_hdr_len, addr):
    """
    print payload data if the source port is 80

    TCP header format: http://www.freesoft.org/CIE/Course/Section4/8.html
    
    """
    shift = ETH_H_LEN + ip_hdr_len
    tcp_h = packet[shift:shift + TCP_H_LEN]
    
    unpacked_tcp_h = struct.unpack('!HHLLBBHHH', tcp_h)
    
    source_port = unpacked_tcp_h[0]
    dst_port = unpacked_tcp_h[1]
    
    if source_port == 80:
        data_offset = unpacked_tcp_h[4]
        tcph_len = (data_offset >> 4) * 4
    
        header_size = tcph_len + ip_hdr_len + ETH_H_LEN
        data_size = len(packet) - header_size
        data = packet[header_size:]
        if data_size != 0 and local_ip == addr[1]:
            parse_payload(data)

def ip_parse(local_ip, packet):
    """
    check if the protocol is TCP. If yes, then parse tcp header
    IPv4 packet format: https://en.wikipedia.org/wiki/IPv4#Packet

    """
    ip_h = packet[ETH_H_LEN:ETH_H_LEN + IP_H_LEN]
    
    unpacked_ip_h = struct.unpack('!BBHHHBBH4s4s', ip_h)
    
    ip_first_byte = unpacked_ip_h[0]
    ip_ver = ip_first_byte >> 4
    # Multiply whatever is stored in ihl with 32 to get the total number of bits
    # or with 4 to get the total number of bytes
    ihl = ip_first_byte & 0xF
    ip_hdr_len = ihl * 4

    packet_protocol = unpacked_ip_h[6]
    src_ip = socket.inet_ntoa(unpacked_ip_h[8])
    dst_ip = socket.inet_ntoa(unpacked_ip_h[9])
    
    # If tcp then parse tcp
    if packet_protocol == 6:
        #print "Source: %s" %src_ip
        #print "Dest: %s" %dst_ip
        tcp_parse(local_ip, packet, ip_hdr_len, [src_ip, dst_ip])

def parse(local_ip, packet):
    """
    Parse for ethernet header
    See <linux/if_ether.h> for ethernet header information
    
    """
    eth_h = packet[0:ETH_H_LEN] 
    unpacked_eth = struct.unpack('6s6sH',eth_h)
    p_type = unpacked_eth[2]

    # If IPv4 packet, then parse IP now
    if p_type == 8:
        ip_parse(local_ip, packet)

def listen(local_ip, sock):
    """
    """
    bufsize = 65535

    while True:
        data, addr = sock.recvfrom(bufsize)
        packet_tuple = sock.recvfrom(bufsize)
        parse(local_ip, packet_tuple[0])    

def setup():
    """
    set up a raw socket
    """
    if len(sys.argv) > 1:
        local_ip = sys.argv[1]
    else:
        print "Usage: packet_parser.py [IP_ADDR]"
        sys.exit(1)

    try:
        raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_P_ALL))
    except socket.error as errstr:
        print "Unable to create raw socket"
        print "Error code: %d, message: %s" %(errstr[0], errstr[1])
        sys.exit(1)


    return (local_ip, raw_socket)

if __name__ == "__main__":
    sock_ip = setup()
    local_ip = sock_ip[0]
    raw_sock = sock_ip[1]

    listen(local_ip, raw_sock)
