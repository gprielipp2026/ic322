class Body:
    def __init__(self, data, binary=False):
        self.data = data
        if type(data) != bytes:
            self.data = data.encode()

        self.binary = binary

    def isBinary(self):
        return self.binary

    def tobytes(self):
        # starting to store everything as bytes
        return self.data

    def __str__(self):
        if self.binary:
            return self.data.decode()
        else:
            return str(self.data) 
