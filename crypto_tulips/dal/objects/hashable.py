class Hashable:
    # Returns the object that will be used to get the hash for the blockchain.
    # Since some objects have aditional members this method allows us to remove these non-block related members
    def get_hashable(self): raise NotImplementedError

    # Used to get the hashable version of an object.
    # Use this with a the map function
    @staticmethod
    def get_hashable_callback(hashableObject):
        return hashableObject.get_hashable()