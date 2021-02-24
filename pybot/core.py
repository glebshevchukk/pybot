'''
Basic pub/sub, services, actions defined here.
Use redis as a parameter store and zeromq to do message comms.
'''
import redis
import jsonpickle
import pickle
import zmq
import numpy as np
import time
from pybot.cmn_structs import *


class Bot(object):
    def __init__(self, namespace='bot', **redis_kwargs):
        self.db= redis.Redis()
        self.namespace=namespace
        self.publish_topics=[]
        self.subscribe_topics=[]
        self.manager_key ="%s_%s" %(namespace, 'manager')
        self.topic_key = "%s_%s" %(namespace, 'topics')
        self.manager_dict=None
        self.topics = {}

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
            topics = self.db.hgetall(self.topic_key)
            self.topics={}
            for key,val in topics.items():
                key = key.decode('utf-8')
                val = int(val.decode('utf-8'))
                self.topics[key] = val
    def make_topic(self,topic,port):
        self.db.hset(self.topic_key, topic, port)
        self.refresh_topics()

class ServiceServer(object):
    def __init__(self,bot):
        self.bot = bot

class ServiceClient(object):
    def __init__(self,bot):
        self.bot=bot