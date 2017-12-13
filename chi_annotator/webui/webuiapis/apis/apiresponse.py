class APIResponse(object):
    def __init__(self, data='', code=0, message=''):
        self.data = data
        self.code = code
        self.message = message
