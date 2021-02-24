import jsonpickle
import zmq
import time
from pybot.cmn_structs import *

class ServiceServer(object):
    def __init__(self,bot,callback,service_name):
        self.bot=bot
        self.callback=callback
        self.service_name=service_name
        
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.port = self.socket.bind_to_random_port("tcp://*")
        self.bot.make_service(service_name,self.port)

        while True:
            self.handle_requests()
        
    def handle_requests(self):
        string = self.socket.recv()
        string= string.decode('utf-8')
        
        msg = jsonpickle.decode(string)
        returned_msg = self.callback(msg)
        returned_msg = jsonpickle.encode(returned_msg)
        self.socket.send_string(returned_msg)

class ServiceClient(object):
    def __init__(self,bot,service_name):
        self.bot=bot
        self.service_name=service_name
        
        self.context = zmq.Context()
        self.refresh_socket()

    def refresh_socket(self):
        self.socket = self.context.socket(zmq.REQ)
        if self.service_name not in self.bot.services:
            print("That service has not been published yet.")
            return
        self.port = int(self.bot.services[self.service_name])
        self.socket.connect("tcp://127.0.0.1:%s"% self.port)
        self.bot.refresh()
        
    def call(self,callback):
        self.refresh_socket()
        msg = callback()
        msg = jsonpickle.encode(msg)
        self.socket.send_string(msg)
        string = self.socket.recv()
        string= string.decode('utf-8')
        msg = jsonpickle.decode(string)
        return msg