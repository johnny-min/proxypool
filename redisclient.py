import redis
from random import choice

REDIS_HOST= 'localhost'
REDIS_PORT= 6379
REDIS_PASSWORD= None
REDIS_KEY= 'proxies'
INITALL_SOCRE= 10
MAX_SCORE= 100
MIN_SCORE= 0

class RedisClient(object):
    def __init__(self, *args, **kwargs):
        
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,  password=REDIS_PASSWORD, decode_responses=True)

    def add(self, proxy, score= INITALL_SOCRE):
        """
        添加 proxy
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, {proxy: score})   # 3.x版本中需传入dict

    def random(self):
        """
        随机返回proxy
        """
        result = self.db.zrangebyscore(INITALL_SOCRE, MAX_SCORE, MAX_SCORE) #返回键名为REDIS_KEY的给定元素
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0,100)    #返回键名为REDIS_KEY的前100名元素
            if len(result):
                return choice(result)
            else:
                raise 'PoolEmptyError'
        
    def descrease(self, proxy):
        """
        proxy分值-1，若小于最小值则剔除
        """
        score = self.db.zscore(REDIS_KEY, proxy)    #获取proxy的score
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score)
            return self.db.zincrby(REDIS_KEY,-1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)       #从键名为REDIS_KEY的zset(有序集合)中剔除proxy

    def exists(self, proxy):
        """
        判断proxy是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为最大值
        """
        print('代理', proxy, '可用,设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        返回键名为REDIS_KEY的zset个数
        """
        return self.db.zcard(REDIS_KEY) #返回键名为REDIS_KEY的zset个数

    def all(self):
        """
        返回键名为REDIS_KEY在给定区间(MIN_SCORE, MAX_SCORE)的元素
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)   #返回键名为REDIS_KEY在给定区间(MIN_SCORE, MAX_SCORE)的元素
