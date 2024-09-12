from .version import Version

class Requestline:
    def __init__(self, method, target, version):
        self.method = method
        self.target = target
        self.version = Version(version)

    def getMethod(self):
        return self.method

    def getVersion(self):
        return self.version

    def getURI(self):
        return self.target

    def __str__(self):
        return f'{self.method} {self.target} {str(self.version)}'
