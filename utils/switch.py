class switch(object):
    def __init__(self, value, mode):
        self.value = value
        self.mode = mode
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.fall or (self.mode in args) and len(args) == 1:
            return True
        elif self.value in args and self.mode in args:
            self.fall = True
            return True
        return False
