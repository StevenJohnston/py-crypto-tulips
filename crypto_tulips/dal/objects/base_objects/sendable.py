class Sendable:
    # Returns the object that will be used to send between nodes and wallets
    # Since some objects have aditional members this method allows us to remove these non-block related members
    def get_sendable(self): raise NotImplementedError

    # Used to get the sendable version of an object.
    # Use this with the map function
    @staticmethod
    def get_sendable_callback(sendableObject):
        return sendableObject.get_sendable()