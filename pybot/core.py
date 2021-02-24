'''
Basic pub/sub, services, actions defined here.
Use redis as a parameter store and zeromq to do message comms.
'''
import redis
import jsonpickle
import zmq
import numpy as np
from datetime import datetime
import time
from pybot.cmn_structs import *


class Bot(object):
    def __init__(self, namespace='bot', **redis_kwargs):
        self.db= redis.Redis()
        self.namespace=namespace
        self.publish_topics=[]
        self.subscribe_topics=[]
        self.manager_key ='%s:%s' %(namespace, 'manager')
        self.topic_key = '%s:%s' %(namespace, 'topics')
        self.manager_dict=None
        self.topic_names=list()

    def start(self):
        #first check if manager already exists
        if self.db.exists(self.manager_key):
            self.manager_dict = jsonpickle.decode(self.db.get(self.manager_key))
            #get all current topics
            self.refresh_topics()
            if self.manager_dict['active'] == False:
                self.manager_dict['active'] = True
                dumped_dict = jsonpickle.encode(self.manager_dict)
                self.db.set(self.manager_key,dumped_dict)
        else:
            start_time = time.time()
            self.manager_dict = {'active':True,'start_time':start_time}
            dumped_dict = jsonpickle.encode(self.manager_dict)
            self.db.set(self.manager_key,dumped_dict)

    def refresh_topics(self):
        if self.db.exists(self.topic_key):
            self.topic_names = [elem.decode('utf-8') for elem in self.db.smembers(self.topic_key)]

    def make_topic(self,topic):
        #check that this topic exists in the list, otherwise append
        if topic not in self.topic_names:
            self.db.sadd(self.topic_key, topic)
        self.refresh_topics()

class Publisher(object):
    def __init__(self,bot,port="5556"):
        self.bot=bot
        self.port=port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % self.port)
        
    def single_publish(self,topics:list,msgs:list):
        '''
        Publish a single msg to the current topic. Useful when you don't have a fixed rate that you'd like to send
        information at.
        '''
        if len(topics) != len(msgs):
            print("Number of topics has to equal number of messages")
            return

        for topic,msg in zip(topics,msgs):
            self.bot.make_topic(topic)
            topic_index = self.bot.topic_names.index(topic)
            #now we want to push to the end of that topic
            ser_msg = jsonpickle.encode(msg)
            self.socket.send_string("%d %s" % (topic_index, ser_msg))

    def rate_publish(self,topics:list,rate,callback):
        '''
        Get a msg from the callback and publish responses to the topics at a certain rate.
        '''
        for topic in topics:
            self.bot.make_topic(topic)
        time_elapse = 1./rate
        while True:
            start = time.time()
            msgs = callback()
            for topic,msg in zip(topics,msgs):
                ser_msg = jsonpickle.encode(msg)
                topic_index = self.bot.topic_names.index(topic)
                self.socket.send_string("%d %s" % (topic_index, ser_msg))
                elapsed = time.time() - start
                wait_time = time_elapse - elapsed
                if wait_time > 0:
                    time.sleep(time_elapse - elapsed)  
    
class Subscriber(object):
    def __init__(self,bot,port="5556"):
        self.bot=bot
        self.port=port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:%s" % self.port)

    def single_subscribe(self,topics):
        '''
        Get the latest msg from the current topics. Useful when you don't have a fixed rate that you'd like to get
        info at
        '''
        #check that this topic exists in the list
        msgs = []
        for topic in topics:
            self.bot.make_topic(topic)
            topic_index = self.bot.topic_names.index(topic)
            self.socket.setsockopt(zmq.SUBSCRIBE, topic_index)
            string = self.socket.recv()
            topic, msg = string.split()
            msg = jsonpickle.decode(msg)
            msgs.append(msg)
        return msgs
    def rate_subscribe(self,topics,rate,callback):
        '''
        Get latest messages from topics at specified rate then process it with callback
        '''
        for topic in topics:
            self.bot.make_topic(topic)
        time_elapse = 1./rate
        while True:
            start = time.time()
            for topic in topics:
                topic_index = self.bot.topic_names.index(topic)
                self.socket.setsockopt_string(zmq.SUBSCRIBE, str(topic_index))
                string = self.socket.recv()
                string= string.decode('utf-8')
                index,msg= string.split(" ",1)

                msg = jsonpickle.decode(msg)
                callback(msg)
                elapsed = time.time() - start
                wait_time = time_elapse - elapsed
                if wait_time > 0:
                    time.sleep(time_elapse - elapsed)  


class ServiceServer(object):
    def __init__(self,bot):
        self.bot = bot

class ServiceClient(object):
    def __init__(self,bot):
        self.bot=bot