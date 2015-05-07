
class Door:
    def __init__(self):
        pass

class EnchantedDoor:
    def __init__(self):
        Door.__init__(self)

class FakeDoor:
    def __init__(self):
        pass

class Maze:
    def __init__(self):
        self.doors = []
        self.rooms = []
    
    def makeDoor(self):
        #return Door()
        # Your code here
    
    def generate(self):
        self.doors.append(self.makeDoor())
        self.doors.append(self.makeDoor())

class EnchantedMaze(Maze):
    def makeDoor(self):
        #return EnchantedDoor()
        # Your code here
    
    def generate(self):
        Maze.generate(self)
        print("Enchanting!")

em = EnchantedMaze()
em.generate()
