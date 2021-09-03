"""
Create a class ''Point'' that stores an x and a y attribute
Update ''Point'' so that it keeps track of how many points have been created
using decorators
"""

import unittest

def counter(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper

class Point():
    @counter
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TestClass(unittest.TestCase):
    def test_class(self):

        p = Point(2, 3)
        self.assertEqual(Point.__init__.count, 1)
        p2 = Point(3, 4)
        self.assertEqual(Point.__init__.count, 2)

if __name__ == '__main__':
    unittest.main()
