'''
Actual driver that you call to start up the realsense and get it publishing
'''
from pybot import RedisBot, Header
from pybot.interfaces import RealSense
import threading

rate = 10.

def launch_realsense():
    bot = RedisBot()
    bot.start()
    rs = RealSense()
    topics = ["rs_image","rs_depth","rs_intrin"]
    pub_thread = threading.Thread(target=bot.rate_publish, args=(topics,rate,rs.__next__,))
    pub_thread.start()
    pub_thread.join()

if __name__ == "__main__":
    launch_realsense()