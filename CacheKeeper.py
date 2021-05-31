import pickle

from answer import Answer, get_current_seconds
class CacheKeeper:
    def __init__(self):
        self.cache = dict()

        self.cache[("1.0.0.127.in-addr.arpa", "000c")] = [Answer("000c", "03646e73056c6f63616c00", "100")]

        self.prev_check_time = get_current_seconds()

    def clear_cache(self):
        global prev_check_time
        current_time = get_current_seconds()
        if current_time - self.prev_check_time >= 120:
            keys_to_delete = []
            for k, v in self.cache.items():
                for item in v:
                    if item.valid_till <= current_time:
                        del item
                if len(v) == 0:
                    keys_to_delete.append(k)
            for k in keys_to_delete:
                del self.cache[k]
            prev_check_time = get_current_seconds()

        with open("backup", "wb+") as f:
            pickle.dump(self.cache, f)