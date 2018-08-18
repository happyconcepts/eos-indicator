# Unit tests for eos-investor
# https://github.com/happyconcepts/eos-investor

# python -m unittest test_binance

import eos_investor
import unittest

class TestEOSInvestor(unittest.TestCase):

    # test reference
    def test_Add(self):
	    result = eos_investor.add(10,5)
	    self.assertEqual(result, 15)

    # test binance API
    def test_Binance(self):
	    b = eos_investor.binance()
	    result = b.run()
	    self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
