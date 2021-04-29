'''
Actual driver that you call to start up the realsense and get it publishing
'''
from pybot import Bot, Header,Publisher
from pybot.interfaces import RealsenseInterface
import threading

rate = 10.

def launch_realsense():
    bot = Bot()
    bot.start()
    pub = Publisher(bot,"/rs")
    rs = RealsenseInterface()
    pub.rate_publish(rate,rs.__next__)

if __name__ == "__main__":
    launch_realsense()
