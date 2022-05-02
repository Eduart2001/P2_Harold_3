import unittest
import db

class TestDataBaseMethods(unittest.TestCase):
    
    def test_graph0(self):
        d = {2020: 181, 2010: 1881, 2000: 1219, 1990: 504}
        self.assertEqual(db.graph0(), d)

    def test_graph1(self):
        d1 = {'03/10/1990': 1, '10/10/1990': 1, '11/10/1990': 1, '01/11/1990': 1, '06/11/1990': 1, '07/11/1990': 1, '09/11/1990': 2, '18/11/1990': 1, '19/11/1990': 1, '07/12/1990': 1, '16/12/1990': 1, '18/12/1990': 1}
        d2 = {'12/12/2000': 1, '26/11/2001': 1, '11/02/2003': 1, '09/09/2003': 1, '16/02/2004': 1, '05/12/2004': 1, '09/12/2004': 1, '18/11/2005': 1, '16/12/2005': 2, '10/05/2006': 1, '11/11/2006': 1, '19/12/2006': 1, '17/02/2007': 1, '16/06/2007': 1, '23/06/2007': 1, '06/10/2007': 1, '27/11/2007': 1, '09/01/2008': 1, '09/09/2008': 1, '02/10/2008': 1, '06/12/2008': 1, '12/01/2009': 1, '26/01/2009': 1, '04/02/2009': 1, '14/12/2009': 1, '19/01/2010': 1, '23/01/2010': 1}
        d3 = {'20/09/1999': 1, '23/01/2000': 1, '29/08/2000': 1, '08/09/2000': 1, '11/09/2000': 1, '03/11/2000': 1, '21/04/2001': 1, '06/10/2001': 1, '11/10/2001': 1}
        self.assertEqual(db.graph1("01/01/1990","12/1990"), d1)
        self.assertEqual(db.graph1("03/10/2000","11/2010","Bleuet"), d2)
        self.assertEqual(db.graph1("18/05/1999","11/2001","Bimbo"), d3)

    def test_graph2(self):
        d4 = -1
        d5 = {'full': 6, 'other': 117}
        d6 = {'other': 2}
        self.assertEqual(db.graph2(1998,7), d4)
        self.assertEqual(db.graph2(2000, None, None, "both"), d5)
        self.assertEqual(db.graph2(2000, None, "Citron", "other"), d6)

    def test_graph3(self):
        d7 = {'Holstein': 0, 'Blanc Bleu Belge': 10}
        d8 = {'Holstein': 155, 'Blanc Bleu Belge': 113, 'Jersey': 14}
        d9 = {'Holstein': 4266}
        self.assertEqual(db.graph3(1,2,None,25,True), d7)
        self.assertEqual(db.graph3(1,2,3,50,True), d8)
        self.assertEqual(db.graph3(1,None,None,100,False), d9)

if __name__ == '__main__':
    unittest.main()