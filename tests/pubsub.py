from pybot import RedisBot, make_header
import random
import threading
import numpy as np

topic = ['testing','tester']
rate = 1000.

def random_callback():
    return [make_header(),make_header()]

def print_callback(msg):
    print(msg)

def test_rate_pub_sub():
    bot = RedisBot()
    bot.start()
    pub_thread = threading.Thread(target=bot.rate_publish, args=(topic,rate,random_callback,))
    sub_thread = threading.Thread(target=bot.rate_subscribe, args=(topic,rate,print_callback,))
    pub_thread.start()
    sub_thread.start()
    pub_thread.join()
    sub_thread.join()

def test_single_pub_sub():
    bot = RedisBot()
    bot.start()
    for i in range(1000):
        bot.publish(topic,i)
        msg = bot.subscribe(topic)
        print(msg)

if __name__ == "__main__":
    #test_single_pub_sub()
    test_rate_pub_sub()