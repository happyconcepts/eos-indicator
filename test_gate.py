# Unit tests for EOS-indicator
# https://github.com/happyconcepts/eos-indicator
# EOS-indicator copyright 2018 ben bird

# python -m unittest test_gate

import unittest
import eos_indicator

class TestEOSIndicator(unittest.TestCase):

    def setUpModule():

	print ("in setUpModule()")

    def test_Add(self):
	result = eos_indicator.add(10,5)
	self.assertEqual(result, 15)

    def test_Gate(self):
	g = eos_indicator.gate()
	result = g.run()
	self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()

