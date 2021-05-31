from CacheKeeper import CacheKeeper
from GetNamer import GetNamer
from answer import get_all_responses
from utils import decimal_to_hex, send_udp_message


class RequestParser:
    def __init__(self, cache_keeper: CacheKeeper):
        self.namer = GetNamer()
        self.ck = cache_keeper
    def parse_request(self, request):
        header = request[0:24]
        question = request[24:]

        name, _ = self.namer.get_name(request)

        t = question[-8: -4]

        if (name, t) in self.ck.cache:
            content, count = get_all_responses(self.ck.cache[(name, t)])

            if count != 0:
                _id = header[0:4]
                flags = "8180"
                qd_count = header[8:12]
                an_count = decimal_to_hex(count).rjust(4, '0')
                ns_count = header[16:20]
                ar_count = header[20:24]

                new_header = _id + flags + qd_count + an_count + ns_count + ar_count

                print(f"name {name} type '{t}' record returned from cache")

                return new_header + question + content

        print(f"name {name} type '{t}' record returned from server")

        return send_udp_message(request, "192.168.0.1", 53)