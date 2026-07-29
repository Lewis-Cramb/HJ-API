class item:
    def __init__(self, height, length, width, weight):
        self.height = height
        self.length = length
        self.width = width
        self.weight = weight

    def getHeight(self):
        return self.height

    def getLength(self):
        return self.length 

    def getWidth(self):
        return self.width

    def getWeight(self):
        return self.weight

class Box(item):
    def __init__(self):
        item.__init__(self, 12, 119, 60, 9.6)

class Cushion(item):
    def __init__(self):
        item.__init__(self, 50, 50, 7, 2)