from SendingMusic import SendingMusic

class Process:
    def __init__(self, filename):
        self.filename = filename

    def start(self):
        sm = SendingMusic(self.filename)
        sm.sending()
