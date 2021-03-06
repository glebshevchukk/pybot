from pybot import Bot, Publisher,Subscriber,ServiceServer,ServiceClient,make_header,make_random_pose,CameraInfo
import random
import threading
import numpy as np

topic = ['main_camera']
rate = 1.

def random_callback():
    return make_random_pose()

def camera_callback():
    pose = make_random_pose()
    info = CameraInfo(width=700,height=500)
    return {"vizType":"camera","pose":pose,"camera":info}

def print_callback(msg):
    print(msg)

def get_beep():
    return "beep"

def ret_beep_boop(msg):
    return msg + " boop"


def launch_publisher(bot):
    pub = Publisher(bot,'main_camera')
    pub.rate_publish(rate,camera_callback)

def launch_subscriber(bot):
    sub = Subscriber(bot)
    sub.rate_subscribe(topic,rate,print_callback)

def launch_client(bot):
    client = ServiceClient(bot,'testing_service')
    for i in range(10):
        ret = client.call(get_beep)
        print(ret)

def launch_server(bot):
    server = ServiceServer(bot,ret_beep_boop,'testing_service')

def test_rate_pub_sub():
    bot = Bot()
    bot.start()
    pub_thread = threading.Thread(target=launch_publisher, args=(bot,))
    sub_thread = threading.Thread(target=launch_subscriber, args=(bot,))
    pub_thread.start()
    sub_thread.start()
    sub_thread.join()
    pub_thread.join()


def test_service_client():
    bot = Bot()
    bot.start()
    server_thread = threading.Thread(target=launch_client, args=(bot,))
    client_thread = threading.Thread(target=launch_server, args=(bot,))
    client_thread.start()
    server_thread.start()
    client_thread.join()
    server_thread.join()


if __name__ == "__main__":
    test_rate_pub_sub()
    #test_service_client()
