# TP4_Minesweeper unittest
# does not work with other version
import unittest
from TP4_Minesweeper import Button

class ButtonLocal(Button):
    def __init__(self, x, y, i, bomb):
        self.x = x
        self.y = y
        self.index = i
        self.isBomb = bomb

class buttonTest(unittest.TestCase):
    def test_count(self):
        x = 3
        y = 3
        buttonLst = [ButtonLocal(i%x, i//x, i,  True) for i in range(9)]

        item = str(buttonLst[4])
        expected = "((1, 1), 4, bomb = True)"
        self.assertEqual(expected, item)

        item = str(buttonLst[0])
        expected = "((0, 0), 0, bomb = True)"
        self.assertEqual(expected, item)

        item = str(buttonLst[7])
        expected = "((1, 2), 7, bomb = True)"
        self.assertEqual(expected, item)

if __name__ == "__main__":
    unittest.main()

        
