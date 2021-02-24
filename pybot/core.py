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
        self.service_key = "%s_%s" %(namespace, 'services')
        self.action_key = "%s_%s" %(namespace, 'actions')
        self.manager_dict=None
        self.topics = {}
        self.services = {}
        self.actions = {}

    def start(self):
        #first check if manager already exists
        if self.db.exists(self.manager_key):
            self.manager_dict = jsonpickle.decode(self.db.get(self.manager_key))
            #get all current topics/services/actions from redis
            self.refresh()
            if self.manager_dict['active'] == False:
                self.manager_dict['active'] = True
                dumped_dict = jsonpickle.encode(self.manager_dict)
                self.db.set(self.manager_key,dumped_dict)
        else:
            start_time = time.time()
            self.manager_dict = {'active':True,'start_time':start_time}
            dumped_dict = jsonpickle.encode(self.manager_dict)
            self.db.set(self.manager_key,dumped_dict)

    def refresh(self):
        for i,key in enumerate([self.topic_key,self.service_key,self.action_key]):
            if self.db.exists(key):
                redis_dic = self.db.hgetall(key)
                dic={}
                for key,val in redis_dic.items():
                    key = key.decode('utf-8')
                    val = int(val.decode('utf-8'))
                    dic[key] = val
                if i == 0:
                    self.topics = dic
                elif i == 1:
                    self.services = dic
                else:
                    self.actions = dic

    def make_topic(self,topic,port):
        self.db.hset(self.topic_key, topic, port)
        self.refresh()

    def make_service(self,service,port):
        self.db.hset(self.service_key, service, port)
        self.refresh()
    
    def make_action(self,action,port):
        self.db.hset(self.action_key, action, port)
        self.refresh()