from pybot import Bot, Publisher,Subscriber,make_header
import random
import threading
import numpy as np

topic = ['testing']
rate = 1.

def random_callback():
    return make_header()

def print_callback(msg):
    print(msg)


def launch_publisher(bot):
    pub = Publisher(bot,'testing')
    pub.rate_publish(rate,random_callback)

def launch_subscriber(bot):
    sub = Subscriber(bot)
    sub.rate_subscribe(topic,rate,print_callback)

def test_rate_pub_sub():
    bot = Bot()

    bot.start()
    pub_thread = threading.Thread(target=launch_publisher, args=(bot,))
    sub_thread = threading.Thread(target=launch_subscriber, args=(bot,))
    pub_thread.start()
    sub_thread.start()
    sub_thread.join()
    pub_thread.join()


if __name__ == "__main__":
    test_rate_pub_sub()