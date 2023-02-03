class Hex:
    def __init__(self, *args):
        pass
    
    @staticmethod
    def corners():
        return []

class PointHex(Hex):
    def __init__(self, *args):
        super().__init__(*args)

class LineHex(Hex):
    def __init__(self, *args):
        super().__init__(*args)

class TextMapper:
    def __init__(self):
        pass

    def make_region(self):
        return PointHex(*args)

    def make_line(self):
        return LineHex(*args)

    def shape(self, attributes):
        points = " ".join([
            f"{x[0]},{x[1]}" for x in Hex.corners()
        ])
        return f"<polygon {attributes} points='{points}' />"

    def viewbox(self, minx, miny, maxx, maxy):
        dx = 0
        dy = 0
        return [int(x) for x in (
            minx * dx * 3/2 - dx - 60,
            (miny - 1.5) * dy,
            maxx * dx * 3/2 + dx + 60,
            (maxy + 1) * dy
        )]
