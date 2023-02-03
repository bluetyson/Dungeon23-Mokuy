
class Point:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.type = None
        self.label = None
        self.size = None
        self.map = None

    def equal(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
        
    def cmp(a, b):
        return (a.x - b.x) or (a.y - b.y) or (a.z - b.z)

    def coordinates(self):
        if self.z is not None:
            return self.x, self.y, self.z
        return self.x, self.y

    def coord(x, y, separator=''):
        return "{:0{}d}{}{:0{}d}".format(
            (3 if x < 0 else 2), x, separator,
            (3 if y < 0 else 2), y
        )