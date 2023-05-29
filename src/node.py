class NodeCore(object):
    def __init__(self, config):
        self.client= None
        self.config = config

    def set_client(self, fn):
        self.client = fn

    async def connected_cb(self, *args):
        pass

    def disconnected_cb(self):
        pass

    def subscribe_cb(self, *args):
        pass


    
