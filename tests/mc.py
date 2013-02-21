from datetime import datetime

def LogError(msg):
    print str(datetime.now()) + ", " + str(msg)

def ShowDialogNotification(msg, icon):
    LogError("notification")

def ActivateWindow(nr):
    LogError("Activating window " + str(nr))
