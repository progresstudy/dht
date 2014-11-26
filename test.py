
class A:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __hash__(self):
        return hash(self.a)

    def __eq__(self, o):
        return self.a == o.a


m1 = A("a", 1)
m2 = A("a", 2)

mm = set()

mm.add(m1)

for i in mm:
    print i.b

mm.add(m2)

for i in mm:
    print i.b

def aa(a, b, c):
    print a
    print b
    print c

cc = (11,22)
aa("cc", *cc)

for i in range(3):
    print i
else:
    print "xxxx"
