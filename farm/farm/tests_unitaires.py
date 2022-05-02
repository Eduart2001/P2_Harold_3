import unittest
import db

class TestDataBaseMethods(unittest.TestCase):
    
    def graph0(self):
        d = None
        self.assertEqual(db.graph0(), d)

    def graph1(self):
        d1 = None
        d2 = None
        d3 = None
        self.assertEqual(db.graph1(startDate,endDate,famille=None), d1)

    def graph2(self):
        d4 = None
        d5 = None
        d6 = None
        self.assertEqual(db.graph2(year=None,month=None,famille=None,fullmoon=None), d4)

    def graph3(self):
        pass