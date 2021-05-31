import pickle

from CacheKeeper import CacheKeeper
from GetNamer import GetNamer
from answer import Answer


class ResponseParser:
    def __init__(self, namer: GetNamer, ck: CacheKeeper):
        self.namer = namer
        self.ck = ck
    def parse_response(self, r):
        if r is None:
            return None

        header = r[0:24]
        question = r[24:]

        name, offset = self.namer.get_name(r)

        t = question[offset - 8: offset - 4]

        dot_count = name.count(".")
        char_count = len(name) - dot_count
        question_len = char_count * 2 + (dot_count + 2) * 2

        answer = r[24 + question_len + 8:]

        an_count = int(header[12:16], 16)
        ns_count = int(header[16:20], 16)
        ar_count = int(header[20:24], 16)

        counts = [an_count, ns_count, ar_count]

        rest = answer

        for count in counts:
            answers = []

            prev_n = name
            n = name

            for i in range(count):
                n = self.namer.extract_name(r, r.index(rest))
                t = rest[4:8]
                ttl = rest[12:20]
                data_len = rest[20:24]

                data_length = int(data_len, 16) * 2
                data = rest[24:24 + data_length]

                link = str(bin(int(data[-4:], 16)))[2:]
                if t == "0002" and data[-2:] != "00" and link[:2] == "11":
                    link = int(link[2:], 2) * 2
                    _, offset = self.namer.get_name(r[link:], 0)
                    ending = r[link:link + offset] + "00"
                    data = data[:-4] + ending

                ans = Answer(t, data, ttl)

                rest = rest[24 + data_length:]

                if n != prev_n:
                    self.ck.cache[(n, t)] = [ans]
                    answers = []
                else:
                    answers.append(ans)

                prev_n = n

            if len(answers) != 0:
                self.ck.cache[(n, t)] = answers

        with open("backup", "wb+") as f:
            pickle.dump(self.ck.cache, f)

        return r