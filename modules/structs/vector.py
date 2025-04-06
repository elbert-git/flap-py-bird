class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    def __repr__(self):
        return [self.x, self.y]
    def __str__(self):
        return f"Vec2( x: {self.x}, y: {self.y})"
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    def multiply_with_vector(self, other):
        return Vector2(
            self.x * other.x,
            self.y * other.y
        )
    def to_tuple(self):
        return (self.x, self.y)