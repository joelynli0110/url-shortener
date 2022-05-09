from src.counter import Counter

class AppServer(object):
    """An AppServer with an unique id contains a counter"""
    def __init__(self,server_id):
        self.id = server_id
        self.counter = Counter(self.id)

    def get_counter_value(self):
        zk_counter = self.counter.zk_counter
        return zk_counter.value

    def __eq__(self, other):
        return self.id == other.id