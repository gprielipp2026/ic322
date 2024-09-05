class Endpoint:
    def __init__(self, method, target, func):
        self.method = method
        self.target = target
        self.func = func

    def match(self, method, target):
        return self.target in target and self.method == method
    
    def handleRequest(self, request):
        return self.func(request)
