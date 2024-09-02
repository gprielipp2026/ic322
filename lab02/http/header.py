class Header:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def matches(self, name):
        return self.name == name

    def getValue(self):
        return self.value

    def __str__(self):
        return f'{self.name}: {self.value}'
