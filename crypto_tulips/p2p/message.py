class Message():
    action = ''
    data = None

    def __init__(self, action, data):
        self.action = action
        self.data = data