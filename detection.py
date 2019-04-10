from redisclient import RedisClient
import asyncio,aiohttp,time
from aiohttp.client_exceptions import ClientConnectionError,ClientError

VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100

class Tester(object):
    def __init__(self, *args, **kwargs):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):

        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://'+ proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理', proxy, '可用')
                    else:
                        self.redis.descrease(proxy)
                        print('代理', proxy, '不可用')
            except (ClientError, ClientConnectionError, TimeoutError, AttributeError):
                self.redis.descrease(proxy)
                print('代理请求失败', proxy)

    def run(self):

        print('开始检测代理')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies),BATCH_TEST_SIZE):
                test_proxies = proxies[1:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('检测器发生错误', e)