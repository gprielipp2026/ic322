from version import Version

class Startline:
    def __init__(self, method, target, version):
        self.method = method
        self.target = target
        self.version = Version(version)

    def __str__(self):
        return f'{self.method} {self.target} {str(self.version)}'
