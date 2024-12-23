
# class Point2d:
#     # __slot__ = ["x", "y"]

#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
    
#     def __add__(self, other: 'Point2d') -> 'Point2d':
#         if isinstance(other, Point2d):
#             return Point2d(self.x + other.x, self.y + other.y)
#         return NotImplemented

#     def __sub__(self, other: 'Point2d') -> 'Point2d':
#         if isinstance(other, Point2d):
#             return Point2d(self.x - other.x, self.y - other.y)
#         return NotImplemented

#     def __mul__(self, scalar: float) -> 'Point2d':
#         return Point2d(self.x * scalar, self.y * scalar)

#     def __truediv__(self, scalar: float) -> 'Point2d':
#         return Point2d(self.x / scalar, self.y / scalar)

#     def __eq__(self, other: 'Point2d') -> bool:
#         return self.x == other.x and self.y == other.y

#     def __str__(self) -> str:
#         return f"Point2d({self.x}, {self.y})"

#     def __repr__(self) -> str:
#         return f"Point2d({self.x}, {self.y})"



