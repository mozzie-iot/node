class NodeCore(object):
    def __init__(self):
        self.client= None

    def set_client(self, fn):
        self.client = fn

    def connected_cb(self, *args):
        pass

    def disconnected_cb(self):
        pass

    def subscribe_cb(self, *args):
        pass


    
