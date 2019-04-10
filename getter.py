from redisclient import RedisClient
from getproxy import Crawler
import sys

POOL_UPPER_THRESHOLD = 10000

class Getter():
    def __init__(self, *args, **kwargs):
        self.redis = RedisClient()
        self._crawler = Crawler()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        print('开始获取')
        if not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self._crawler.get_raw_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add(proxy)