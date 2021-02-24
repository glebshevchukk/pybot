import redis
import jsonpickle
import numpy as np
from datetime import datetime
import time
from pybot.cmn_structs import *
from pybot.queues import *


class RedisBot(object):
    def __init__(self, namespace='bot', **redis_kwargs):
        self.__db= redis.Redis()
        self.namespace=namespace
        self.publish_topics=[]
        self.subscribe_topics=[]
        self.manager_key ='%s:%s' %(namespace, 'manager')
        self.topic_key = '%s:%s' %(namespace, 'topics')
        self.manager_dict=None
        self.topics={}

    def start(self):
        #first check if manager already exists
        if self.__db.exists(self.manager_key):
            self.manager_dict = jsonpickle.decode(self.__db.get(self.manager_key))
            #get all current topics
            self.refresh_topics()
            if self.manager_dict['active'] == False:
                self.manager_dict['active'] = True
                dumped_dict = jsonpickle.encode(self.manager_dict)
                self.__db.set(self.manager_key,dumped_dict)
        else:
            start_time = time.time()
            self.manager_dict = {'active':True,'start_time':start_time}
            dumped_dict = jsonpickle.encode(self.manager_dict)
            self.__db.set(self.manager_key,dumped_dict)

    def refresh_topics(self):
        if self.__db.exists(self.topic_key):
            topic_names = self.__db.smembers(self.topic_key)
            for topic_name in topic_names:
                if topic_name not in self.topics:
                    self.topics[topic_name] = RedisLIFOQueue(self.__db,self.namespace,topic_name)

    def single_publish(self,topics,msgs):
        '''
        Publish a single msg to the current topic. Useful when you don't have a fixed rate that you'd like to send
        information at.
        '''
        if len(topics) != len(msgs):
            print("Number of topics has to equal number of messages")
            return

        for topic,msg in zip(topics,msgs):
            self.make_topic_for_publish(topic)
            #now we want to push to the end of that topic
            q = self.topics[topic]
            ser_msg = jsonpickle.encode(msg)
            q.put(ser_msg)

    def single_subscribe(self,topics):
        '''
        Get the latest msg from the current topics. Useful when you don't have a fixed rate that you'd like to get
        info at
        '''
        #check that this topic exists in the list
        msgs = []
        for topic in topics:
            if not self.exists_topic(topic):
                return None
            if topic not in self.topics.keys():
                print("The topic you have subscribed to has not been published to yet.")
                return None
            q = self.topics[topic]
            #now we want to push to the end of that topic
            msg = q.get()
            msg = jsonpickle.decode(msg)
            msgs.append(msg)
        return msgs

    def rate_publish(self,topics,rate,callback):
        '''
        Get a msg from the callback and publish responses to the topics at a certain rate.
        '''
        qs= []
        for topic in topics:
            self.make_topic_for_publish(topic)
            qs.append(self.topics[topic])
        time_elapse = 1./rate
        while True:
            start = time.time()
            msgs = callback()
            for q,msg in zip(qs,msgs):
                ser_msg = jsonpickle.encode(msg)
                q.put(ser_msg)
                elapsed = time.time() - start
                wait_time = time_elapse - elapsed
                if wait_time > 0:
                    time.sleep(time_elapse - elapsed)  
    
    def rate_subscribe(self,topics,rate,callback):
        '''
        Get latest messages from topics at specified rate then process it with callback
        '''
        qs = []
        for topic in topics:
            self.exists_topic_for_subscribe(topic)
            qs.append(self.topics[topic])
        time_elapse = 1./rate
        while True:
            start = time.time()
            for q in qs:
                msg = q.get()
                msg = jsonpickle.decode(msg)
                callback(msg)
                elapsed = time.time() - start
                wait_time = time_elapse - elapsed
                if wait_time > 0:
                    time.sleep(time_elapse - elapsed)  

    def exists_topic_for_subscribe(self,topic):
        self.refresh_topics()
        #check that this topic exists in the list
        if topic not in self.topics.keys():
            print("The topic you have subscribed to has not been published to yet.")
            return False

    def make_topic_for_publish(self,topic):
        self.refresh_topics()
        #check that this topic exists in the list, otherwise append
        if topic not in self.topics.keys():
            self.__db.sadd(self.topic_key, topic)
            self.topics[topic]=RedisLIFOQueue(self.__db,self.namespace,topic)


