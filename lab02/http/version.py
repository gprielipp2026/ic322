class Version:
    def __init__(self, string):
        self.protocol, self.version = string.split("/")

    def tobytes(self):
        return str(self).encode()

    def __str__(self):
        return f'{self.protocol}/{self.version}'
