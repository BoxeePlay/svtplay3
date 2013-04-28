import threading
from logger import BPLog, Level

'''
Job Manager Object
'''
class BoxeeJobManager(threading.Thread):
    def __init__(self, interval=10, limit=18000):
        self.jobs = []
        self.elapsed = 0
        self.fault = False
        self.timer = threading.Event()
        self.interval = interval
        self.limit = limit
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.log("Initialized.")

    def stop(self):
        self.log("Stop command received.")
        self.fault = True
        return self.fault

    def run(self):
        # Main loop
        while self.fault is False:
            self.timer.wait(self.interval)
            self.elapsed = self.elapsed + self.interval
            try:
                self.process()
            except Exception, e:
                self.stop()
                raise JobError("Encountered running job queue.", e)
            self.check()
            # Hard limit on length of Job Manager (default five hours)
            if self.elapsed == self.limit:
                self.stop()

    def process(self):
        # Process job queue
        if self.jobs:
            for job in self.jobs:
                if job.elapsed >= job.interval:
                    self.log("Processing job: %s" % (job.name))
                    try:
                        job.process()
                        job.elapsed = 0
                        if not job.repeat:
                            self.jobs.remove(job)
                    except Exception, e:
                        raise JobError("Encountered error with job: %s" % (job.name), e)
                else:
                    job.elapsed = job.elapsed + self.interval
                    self.log("Skipping job: %s" % (job.name))

    def addJob(self, boxee_job):
        self.log("Adding new job: %s" % (boxee_job.name))
        return self.jobs.append(boxee_job)

    def check(self):
        # Extend this function to run your own check to see if loop should keep running.
        return

    def log(self, message):
        BPLog("BoxeeJobManager: %s" % (str(message)), Level.DEBUG)

    def error(self, message):
        BPLog("BoxeeJobManager: %s" % (str(message)), Level.ERROR)


'''
Object for Jobs

Extend this object and pass to JobManager object to queue up the job.
'''
class BoxeeJob(object):
    def __init__(self, name, interval=10, repeat=False):
        self.name = name
        self.interval = interval
        self.elapsed = 0
        self.repeat = repeat

    def run(self):
        # Error-safe wrapper for user-defined job logic
        try:
            self.process()
        except Exception, e:
            raise JobError("%s failed:" % (self.name), e)

    def process(self):
        '''
        Main function launched with each job.
        '''
        return

    def log(self, message):
        BPLog("BoxeeJob %s: %s" % (self.name, str(message)), Level.DEBUG)

    def error(self, message):
        BPLog("BoxeeJob %s: %s" % (self.name, str(message)), Level.ERROR)


'''
Boxee Job Manager Exception
'''
class JobError(Exception):
    def __init__(self, message, e):
        Exception.__init__(self, message)
        self.log(message, e)

    def log(self, message, e):
        BPLog("BoxeeJobManager: %s! %s" % (message, str(e)), Level.ERROR)
