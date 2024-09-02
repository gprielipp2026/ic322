class Status:
    reasons = None

    def __init__(self, code):
        self.code = code

    @staticmethod
    def load( fn):
        with open(fn, "r") as fd:
            lines = [(int(x[0:4]), x[4:]) for x in fd.readlines()]
            pairs = {}
            for code, reason in lines:
                pairs[code] = reason 
            return pairs

    def __str__(self):
        if Status.reasons == None:
            Status.reasons = Status.load("./http/reasons.txt")
        return str(self.code) + " " + Status.reasons[self.code]
