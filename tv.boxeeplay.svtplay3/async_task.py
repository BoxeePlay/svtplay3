import threading
from logger import BPLog, Level

class AsyncTask(threading.Thread):

    def __init__(self, target, args=(), kwargs={}):
        threading.Thread.__init__(self)
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.setDaemon(True)
        self.returned = None
        self.error = None

    def run(self):
        try:
            self.returned = self.target(*self.args, **self.kwargs)
        except Exception, e:
            self.error = e

    def get_result(self):
        if self.isAlive():
            raise RuntimeError("Not finished yet")
        if self.error is not None:
            raise AsyncError("Error occurred while doing background work", self.error)
        return self.returned

class AsyncError(Exception):
    def __init__(self, message, e):
        Exception.__init__(self, message)
        self.log(message, e)

    def log(self, message, e):
        BPLog("AsyncTask: %s! %s" % (message, str(e)), Level.ERROR)
