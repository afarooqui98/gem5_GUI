"""holds a parent-child connection between two sym_objects. The parent and child
share access to this class object in order to have access to the line
endpoints for redrawing purposes."""

class Connection:

    def __init__(self, parent_endpoint, child_endpoint, parent_port_num,
        child_port_num):
        self.parentEndpoint = parent_endpoint
        self.childEndpoint = child_endpoint
        self.parentPortNum = parent_port_num
        self.childPortNum = child_port_num
        self.line = None

    # sets new endpoints for the line (None passed in if unmodified)
    def setEndpoints(self, parent_endpoint, child_endpoint):
        if parent_endpoint is not None:
            self.parentEndpoint = parent_endpoint
        if child_endpoint is not None:
            self.childEndpoint = child_endpoint
