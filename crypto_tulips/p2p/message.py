class Message():
    action = ''
    data = None

    def __init__(self, action, data):
        self.action = action
        self.data = data

    def to_json(self, is_object=True):
        if is_object:
            return {
                "action" : self.action,
                "data" : self.data.get_sendable()
                }
        else:
            return {
                "action" : self.action,
                "data" : self.data
                }

    @staticmethod
    def from_dict(dic):
        new_msg = Message(action=dic['action'], data=dic['data'])
        return new_msg
