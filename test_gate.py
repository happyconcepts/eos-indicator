# Unit tests for EOS-investor
# https://github.com/happyconcepts/eos-investor
# EOS-investor copyright 2018 ben bird

# python -m unittest test_gate

import unittest
import eos_investor

class TestEOSIndicator(unittest.TestCase):

    def setUpModule():

	print ("in setUpModule()")

    def test_Add(self):
	result = eos_investor.add(10,5)
	self.assertEqual(result, 15)

    def test_Gate(self):
	g = eos_investor.gate()
	result = g.run()
	self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
