def pixels(self, point):
    x = point.x * self.dx * 3/2
    y = (point.y + self.offset[point.z]) * self.dy - point.x % 2 * self.dy/2
    return x, y if isinstance(point, tuple) else "%.1f,%.1f" % (x, y)

delta = [
    [(-1, 0), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1)], # x is even
    [(-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 0)], # x is odd
]

def one_step(self, from_, to):
    delta = self.delta
    min_ = None
    best = None
    for i in range(6):
        x = from_.x + delta[from_.x % 2][i][0]
        y = from_.y + delta[from_.x % 2][i][1]
        d = (to.x - x) ** 2 + (to.y - y) ** 2
        if min_ is None or d < min_:
            min_ = d
            best = Point(x=x, y=y, z=from_.z)
    return best