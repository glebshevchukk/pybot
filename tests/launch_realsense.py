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
    pub = Publisher(bot,"rs_intrin")
    rs = RealsenseInterface()

    #topics = ["rs_image","rs_depth","rs_intrin"]
    pub.rate_publish(rate,rs.__next__)
    #pub_thread = threading.Thread(target=pub.rate_publish, args=(rate,rs.__next__,))
    #pub_thread.start()
    #pub_thread.join()

if __name__ == "__main__":
    launch_realsense()
