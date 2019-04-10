TESTER_CYCLE, GETTER_CYCLE = 20, 20
TESTER_ENABLED, GETTER_ENABLED, API_ENABLED = True, True, True
API_HOST = 'localhost'
API_PORT = 5000

import time
from multiprocessing import Process
from interface import app
from detection import Tester
from getter import Getter

class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):

        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self,cycle=GETTER_CYCLE):

        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_interface(self):
        
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            interface_process = Process(target=self.schedule_interface)
            interface_process.start()