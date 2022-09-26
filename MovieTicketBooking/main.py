from __future__ import annotations


class B:
    def __init__(self, id: int = -90, a: A = None):
        self.id: int = id
        self.a: A = a


class A:
    def __init__(self, id: int = -90, b: B = None):
        self.id: int = id
        self.b: B = b


a = A(324324, B())
b = B(45, a)

print(a)
print(b)
