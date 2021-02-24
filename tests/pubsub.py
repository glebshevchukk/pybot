from pybot import Bot, Publisher,Subscriber,make_header
import random
import threading
import numpy as np

topic = ['testing']
rate = 1000.

def random_callback():
    return [make_header(),make_header()]

def print_callback(msg):
    print(msg)

def test_rate_pub_sub():
    bot = Bot()
    pub = Publisher(bot)
    sub = Subscriber(bot)
    bot.start()
    pub_thread = threading.Thread(target=pub.rate_publish, args=(topic,rate,random_callback,))
    sub_thread = threading.Thread(target=sub.rate_subscribe, args=(topic,rate,print_callback,))
    pub_thread.start()
    sub_thread.start()
    pub_thread.join()
    sub_thread.join()

def test_single_pub_sub():
    bot = Bot()
    bot.start()
    pub = Publisher(bot)
    sub = Subscriber(bot)
    for i in range(1000):
        pub.single_publish(topic,[make_header()])
        msg = sub.single_subscribe(topic)
        print(msg)

if __name__ == "__main__":
    #test_single_pub_sub()
    test_rate_pub_sub()