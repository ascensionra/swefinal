
import random as r

r.seed()

class Door:
    def __init__(self):
        pass

class EnchantedDoor:
    def __init__(self):
        Door.__init__(self)

class FakeDoor:
    def __init__(self):
        pass

class DoorFactory:
    def makeDoor(self):
        return Door()
    
    def __call__(self):
        return self.makeDoor()

class EnchantedDoorFactory(DoorFactory):
    def makeDoor(self):
        return EnchantedDoor()

class FakeDoorFactory(DoorFactory):
    def makeDoor(self):
        return FakeDoor()

class RandomDoorFactory:
    def makeDoor(self):
        if r.randint(0,1):
            return Door()
        return EnchantedDoor()

class Maze:
    def __init__(self):
        self.doors = []
        self.rooms = []
    
    def generate(self, df):
        self.doors.append(df.makeDoor())

m = Maze()
m.generate(DoorFactory())
