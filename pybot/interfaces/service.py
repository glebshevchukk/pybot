import jsonpickle
import zmq
import time
from pybot.cmn_structs import *

class ServiceServer(object):
    def __init__(self,bot,callback,service_name,port="5556"):
        self.bot=bot
        self.port=port
        self.callback=callback
        self.service_name=service_name
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % self.port)

        while True:
            self.handle_requests()
        
    def handle_requests(self):
        self.socket.setsockopt_string(zmq.REP, str(self.service_name))
        string = self.socket.recv()
        string= string.decode('utf-8')
        service, msg = string.split(" ",1)
        msg = jsonpickle.decode(msg)
        returned_msg = callback(msg)
        self.socket.send(returned_msg)