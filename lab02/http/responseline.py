class Responseline:
    def __init__(self, version):
        self.version = version
        self.status = None

    def setStatus(self, status):
        self.status = status

    def __str__(self):
        return str(self.version) + " " + str(self.status)
