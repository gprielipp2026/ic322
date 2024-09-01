class Version:
    def __init__(self, string):
        self.protocol, self.version = string.split("/")

    def __str__(self):
        return f'{self.protocol}/{self.version}'
