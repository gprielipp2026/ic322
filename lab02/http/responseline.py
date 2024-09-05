class Responseline:
    def __init__(self, version):
        self.version = version
        self.status = None

    def setStatus(self, status):
        self.status = status

    def tobytes(self):
        # swithcing to bytes
        return self.version.tobytes() + " ".encode() + self.status.tobytes()

    def __str__(self):
        return str(self.version) + " " + str(self.status)
