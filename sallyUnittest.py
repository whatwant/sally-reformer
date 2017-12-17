import unittest
import sallyReformer

class SallyUtilTest(unittest.TestCase):

    def test_tfile_equalsFirstname(self):
        t = sallyReformer.TFile( '/srv/workspace', 'AAA.BBB.CCC')
        result = t.equalsFirstname('AAA')
        self.assertTrue(result)



if __name__ == '__main__':
    unittest.main()