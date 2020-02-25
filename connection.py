class Connection():

    def __init__(self, pos1, pos2):
        self.endpoint1 = pos1
        self.endpoint2 = pos2


    def setEndpoints(self, endpoint1, endpoint2):
        if endpoint1 is not None:
            self.endpoint1 = endpoint1
        if endpoint2 is not None:
            self.endpoint2 = endpoint2
