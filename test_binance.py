# Unit tests for eos-indicator
# https://github.com/happyconcepts/eos-indicator
# eos-indicator copyright 2018 ben bird

# python -m unittest test_binance

import unittest
import eos_indicator

class TestEOSIndicator(unittest.TestCase):

    def setUpModule():
	print ("in setUpModule()")

    # test test (reference)
    def test_Add(self):
	result = eos_indicator.add(10,5)
	self.assertEqual(result, 15)

    # test binance API
    def test_Binance(self):
	b = eos_indicator.binance()
	result = b.run()
	self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
