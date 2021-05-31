import pickle
from socket import *

from CacheKeeper import CacheKeeper
from GetNamer import GetNamer
from RequestParser import RequestParser
from ResponseParser import ResponseParser
from answer import Answer, get_all_responses, get_current_seconds
import binascii

from utils import send_udp_message, decimal_to_hex

if __name__ == '__main__':
    try:
        with open("backup", "rb") as f:
            cache = pickle.load(f)
    except:
        print("backup file not found")

    host = 'localhost'
    port = 53
    addr = (host, port)

    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind(addr)

    print(f"started on {addr}")
    namer = GetNamer()
    ck = CacheKeeper()
    reqParser = RequestParser(ck)
    resParser = ResponseParser(namer, ck)
    while True:
        received, addr = udp_socket.recvfrom(1024)
        received = binascii.hexlify(received).decode("utf-8")

        response = resParser.parse_response(reqParser.parse_request(received))

        if response is not None:
            udp_socket.sendto(binascii.unhexlify(response), addr)
        ck.clear_cache()
