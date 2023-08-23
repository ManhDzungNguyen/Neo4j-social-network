import hashlib
from threading import Thread
import time
import numpy as np


class CacheOnRam(object):

    def __init__(self, cache_name: str, max_count: int = -1, expire_time: float = 60):
        self.cache = dict()
        self.cache_name = cache_name
        self.max_count = max_count
        self.expire_time = max(expire_time, 0)
        self.count = 0
        self.worker_check = None
        self.flag = -1

    @staticmethod
    def hash_key(key_cache: str):
        key_cache = hashlib.sha224(key_cache.encode(encoding="utf-8")).hexdigest()
        return key_cache

    def update_cache(self, key_cache: str, val: object = None, expire_time: float = -1):
        k = self.hash_key(key_cache)
        if k not in self.cache:
            self.count += 1
            self.cache[k] = dict()
        if expire_time < 0:
            self.cache[k]["expire_time"] = self.expire_time
        else:
            self.cache[k]["expire_time"] = expire_time
        self.cache[k]["val"] = val
        self.cache[k]["time"] = time.time()

    def get_cache(self, key_cache: str):
        k = self.hash_key(key_cache)
        return self.cache[k]

    def check_cache(self, key_cache: str):
        k = self.hash_key(key_cache)
        if k in self.cache:
            return True
        return False

    def purge_cache(self):
        print("count cache: ", self.count)
        self.cache.clear()
        self.count = 0

    def check_and_remove_cache(self, time_sleep: int = 5):
        while self.flag == 1:
            print("len cache: ", self.count)
            if self.count > self.max_count > 0:
                lst_k = []
                lst_time = []
                keys = list(self.cache.keys())
                for k in keys:
                    lst_k.append(k)
                    lst_time.append(self.cache[k]["time"])
                id_sort = np.argsort(np.array(lst_time))[::-1][self.max_count:]
                lst_k = np.array(lst_k)[id_sort].tolist()
                for k in lst_k:
                    del self.cache[k]
                    self.count -= 1

            keys = list(self.cache.keys())
            for k in keys:
                if time.time() - self.cache[k]["time"] > self.cache[k]["expire_time"]:
                    del self.cache[k]
                    self.count -= 1
            time.sleep(time_sleep)

    def start(self, time_sleep: int = 5):
        if self.flag != 1:
            self.flag = 1
            self.worker_check = Thread(target=self.check_and_remove_cache, args=(time_sleep,))
            self.worker_check.setDaemon(True)
            self.worker_check.start()

    def stop(self):
        self.flag = 0


if __name__ == '__main__':
    cache_test = CacheOnRam("cache_test", max_count=5, expire_time=10)
    cache_test.start()
    st_time = time.time()
    while True:
        vall = time.time()
        cache_test.update_cache("key_{0}".format(str(vall)), val=vall)
        time.sleep(2)
        if time.time() - st_time > 120:
            cache_test.stop()
        print(len(cache_test.cache))
        if time.time() - st_time > 240:
            cache_test.purge_cache()
            print("after purge: ", len(cache_test.cache))
