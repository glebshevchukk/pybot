class RedisLIFOQueue(object):
    def __init__(self, db,namespace,topic,max_size=1000):
        self.__db= db
        self.namespace=namespace
        self.topic=topic
        self.key = '%s:%s' %(namespace, topic)
        self.max_size = max_size

    def size(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.size() == 0

    def put(self, item):
        self.__db.rpush(self.key, item)
        

    def get(self):
        return self.__db.lindex(self.key,-1)