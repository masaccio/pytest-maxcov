class Add:
    def __init__(self):
        self._a = 10
        self._b = 20

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    def add(self, double=False):
        if double:
            return (self.a + self.b) * 2
        else:
            return self.a + self.b
