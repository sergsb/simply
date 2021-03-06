#import redis
import time
from multiprocessing import Process

import pytest

from simply import SimplyRedisClient
from simply.simplyRPCServer import SimplyRedisServer


class SimpleTest(SimplyRedisServer):
    @SimplyRedisServer.rpc
    def add(x, y):
        return x + y

    @SimplyRedisServer.rpc
    def delayed_count(n):
        for i in range(n):
            time.sleep(1)
        return 42

    @SimplyRedisServer.rpc
    def hello(name):
        return "hello, {}".format(name)


def run_simple_test():
    server = SimpleTest("redis://localhost:6379", 'test','mock')
    server.run()

def test_instant():
    x = Process(target=run_simple_test)
    x.start()
    c = SimplyRedisClient("redis://localhost:6379",'test','mock')
    assert c.call('add',[1,2],{}) == 3
    assert c.call('hello',[],{'name':'simply'}) == b"hello, simply"
    #assert c.call('delayed_count',[3], {},type='delayed') == 42
    #assert c.call('delayed_count',[3], {},type='delayed') == 0
    x.terminate()
    #time.sleep(10)

def test_delayed():
    x = Process(target=run_simple_test)
    x.start()
    #time.sleep(1)
    c = SimplyRedisClient("redis://localhost:6379",'test','mock')
    assert c.call('delayed_count',[5], {},type='delayed') == 42
    x.terminate()

#connection = redis.from_url("redis://localhost:6379")

#while True:
#    _,message = connection.blpop("syntelly_calls")

    #print(message)
#connection.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})
#print(connection.get('Bahamas'))