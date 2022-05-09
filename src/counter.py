from kazoo.client import KazooClient

class Counter(object):
    """
    The counter is assigned to each app server.
    """
    def __init__(self, range_idx, counter_size=1000000):
        self.counter_size = counter_size
        self.range_idx = range_idx
        self.init_value = range_idx * counter_size
        # The client will connetct to a local Zookeeper server on the default port (2181)
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.start()
        # initialize a zk counter with the range index and the default value
        self.zk_counter = zk.Counter(str(self.range_idx),default=self.init_value) 
        
    def add(self):
        zk_counter = self.zk_counter
        zk_counter += 1
        return zk_counter

