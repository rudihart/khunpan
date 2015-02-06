__author__ = 'Rudolf Hart'

class KhunpanError(Exception):
    def __init__(self, errstr):
        self.errstr = errstr

    def __str__(self):
        return repr(self.errstr)


