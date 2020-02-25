# holds a parent-child connection between two sym_objects. The parent and child
# share access to this class object in order to have access to the line
# endpoints for redrawing purposes. More functionality to be added later
class Connection:

    def __init__(self, endpoint1, endpoint2):
        self.endpoint1 = endpoint1
        self.endpoint2 = endpoint2

    # sets new endpoints for the line (None passed in if unmodified)
    def setEndpoints(self, endpoint1, endpoint2):
        if endpoint1 is not None:
            self.endpoint1 = endpoint1
        if endpoint2 is not None:
            self.endpoint2 = endpoint2
