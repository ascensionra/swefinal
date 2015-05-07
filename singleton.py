
def SingletonEager(cls):
    instance = cls()
    def getinstance():
        return instance
    return getinstance

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class Counter:
    def __init__(self):
        self.count = 0
    def inc(self):
        self.count += 1

EagerCounter = SingletonEager(Counter)
OneCounter = SingletonOne(Counter)
Counter = singleton(Counter)

if __name__=="__main__":
    a = Counter()
    b = Counter()
    assert(a is b)
    a.inc()
    assert(b.count == 1)
    
    
    c = EagerCounter()
    d = EagerCounter()
    assert(c is d)
    
    c.inc()
    assert(c.count == d.count)
    assert(c.count == 1)
    
    e = OneCounter()
    f = OneCounter()
    assert(e is f)

