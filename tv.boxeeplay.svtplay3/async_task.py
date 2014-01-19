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
        self.exc_info = None

    def run(self):
        try:
            self.returned = self.target(*self.args, **self.kwargs)
        except Exception:
            import sys
            self.exc_info= sys.exc_info()

    def get_result(self):
        if self.isAlive():
            raise RuntimeError("Not finished yet")
        if self.exc_info:
            raise self.exc_info[1], None, self.exc_info[2]
        return self.returned

class AsyncError(Exception):
    def __init__(self, message, e):
        Exception.__init__(self, message)
        self.log(message, e)

    def log(self, message, e):
        BPLog("AsyncTask: %s! %s" % (message, str(e)), Level.ERROR)
