class A:
    def __init__(self):
        self.a = "A"

    def f1(self):
        print("test " + self.a)

    def f2(self):
        print("mod")

    def bind(self):
        setattr(self, "f1", self.f2)


a = A()
a.bind()
a.f2()
