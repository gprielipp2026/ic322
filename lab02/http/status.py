class Status:
    reasons = None

    def __init__(self, code):
        self.code = code

    @staticmethod
    def load( fn):
        with open(fn, "r") as fd:
            lines = [(int(x[0:4]), x[4:].strip()) for x in fd.readlines()]
            pairs = {}
            for code, reason in lines:
                pairs[code] = reason 
            return pairs

    def tobytes(self):
        if Status.reasons == None:
            Status.reasons = Status.load("./http/reasons.txt")
            #print("Loaded reasons:")
            #print(Status.reasons)

        return str(self.code).encode() + " ".encode() + Status.reasons[self.code].encode()

    def __str__(self):
        if Status.reasons == None:
            Status.reasons = Status.load("./http/reasons.txt")
            #print("Loaded reasons:")
            #print(Status.reasons)

        return str(self.code) + " " + Status.reasons[self.code]
