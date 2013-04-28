from jobmanager import BoxeeJob
import mixpanel_client as tracker

class TrackerJob(BoxeeJob):
    def __init__(self, name, data):
        self.name = name
        self.data = data
        BoxeeJob.__init__(self, name, repeat=False)

    def process(self):
        tracker.track(self.name, self.data)

