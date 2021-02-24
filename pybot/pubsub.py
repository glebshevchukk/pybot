import jsonpickle
import zmq
import time
from pybot.cmn_structs import *


class Publisher(object):
    def __init__(self,bot,topic):
        self.bot=bot

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.port = self.socket.bind_to_random_port("tcp://*")
        self.bot.make_topic(topic,self.port)
        self.topic=topic
        
        
    def single_publish(self,msg:dict):
        '''
        Publish a single msg to the current topic. Useful when you don't have a fixed rate that you'd like to send
        information at.
        '''
        ser_msg = jsonpickle.encode(msg)
        self.socket.send_string(ser_msg)

    def rate_publish(self,rate:int,callback):
        '''
        Get a msg from the callback and publish responses to the topic at a certain rate.
        '''
        time_elapse = 1./rate
        while True:
            start = time.time()
            msg = callback()
            ser_msg = jsonpickle.encode(msg)
            self.socket.send_string(ser_msg)
            elapsed = time.time() - start
            wait_time = time_elapse - elapsed
            if wait_time > 0:
                time.sleep(time_elapse - elapsed)  
    

class Subscriber(object):
    def __init__(self,bot):
        self.bot=bot
    
        self.bot.refresh_topics()
        self.context = zmq.Context()
        self.poller = zmq.Poller()
    
    def get_subscribers(self,topics,callbacks):
        self.bot.refresh_topics()
        subs = []
        val_topics = []
        val_callbacks=[]
        
        for i,topic in enumerate(topics):
            try:
                topic_port = int(self.bot.topics[topic])
            except:
                print(f"Topic port for topic {topic} does not exist, skipping." )
                continue
            new_sub = self.context.socket(zmq.SUB)
       
            new_sub.connect("tcp://127.0.0.1:%s"% topic_port)
            new_sub.setsockopt_string(zmq.SUBSCRIBE, "")
            self.poller.register(new_sub, zmq.POLLIN)
  
            subs.append(new_sub)
            val_topics.append(topic)

            if type(callbacks) is list:
                val_callbacks.append(callbacks[i])
        
        return val_topics,subs,val_callbacks

    def single_subscribe(self,topics):
        '''
        Get the latest msg from the current topics. Useful when you don't have a fixed rate that you'd like to get
        info at
        '''
        msgs = {}    
        val_topics,subs,_ = self.get_subscribers(topics)
        socks = dict(self.poller.poll())

        for val_topic,sub in zip(val_topics,subs):
            if sub in socks:
                string = sub.recv()
                msg= string.decode('utf-8') 
                msg = jsonpickle.decode(msg)
                msgs[val_topic] = msg
        return msgs
    def rate_subscribe(self,topics,rate,callbacks):
        '''
        Get latest messages from topics at specified rate then process it with callback.
        If the callback is a list, then we assume that there is a single callback for each
        topic and call it right after getting that message.
        Otherwise, we assume that the callback is over the aggregate total of all messages.
        '''
        if type(callbacks) is list:
            if len(topics) != len(callbacks):
                print("The number of callbacks does not equal number of topics.")
                return

        val_topics,subs,val_callbacks = self.get_subscribers(topics,callbacks)
        
        time_elapse = 1./rate
        while True:
            start = time.time()
            msgs = {}
            socks = dict(self.poller.poll(zmq.DONTWAIT))
            for i in range(len(val_topics)):
                sub = subs[i]
                val_topic = val_topics[i]
                if sub in socks:
                    string = sub.recv()
                    msg= string.decode('utf-8')
                    msg = jsonpickle.decode(msg)
                    if type(callbacks) is list:
                        val_callbacks[i](msg)
                    else:
                        msgs[val_topic] = msg
            if type(callbacks) is not list:
                callbacks(msgs)

            elapsed = time.time() - start
            wait_time = time_elapse - elapsed
            if wait_time > 0:
                time.sleep(time_elapse - elapsed)  
