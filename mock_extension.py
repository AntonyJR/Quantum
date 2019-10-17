from unittest import TestCase

class MockExtension(TestCase):
    @staticmethod
    def print_result(register):
        print("after  " + register.vector_as_string())
        print(register.states_as_string())
        print("")

    def setUp(self):
        self.num_measures = 100000
        self.state_accuracy_percent = 0.05

    @staticmethod
    def make_state_string(state, num_qbits):
        return "|" + format(state, "0" + str(num_qbits) + "b") + ">"

    @staticmethod
    def error_string(found, expected, msg):
        return msg + " expected " + str(expected) + " found " + str(found)

    def assertEqualWrapper(self, found, expected, msg):
        self.assertEqual(found, expected,
                         self.error_string(found, expected, msg))

    def assertReasonablyEqualWrapper(self, found, expected, percent, msg):
        delta = complex(expected - found)
        tolerance = complex(expected) * complex(percent, percent)
        self.assertTrue(abs(delta.real) <= tolerance.real and abs(delta.imag) <= tolerance.imag,
                        self.error_string(found, expected, msg))

    def assertSequenceEqualWrapper(self, found, expected, msg):
        self.assertSequenceEqual(found, expected,
                                 self.error_string(found, expected, msg))

    def assertReasonablyEqualSequenceWrapper(self, found, expected, percent, msg):
        for i in range(len(found)):
            self.assertReasonablyEqualWrapper(found[i], expected[i], percent, msg + " value")

    def assertEqualDictionaryWrapper(self, found, expected, msg):
        self.assertEqualWrapper(len(found), len(expected), msg + " length")
        fkeys = found.keys()
        for key in expected.keys():
            self.assertTrue(key in fkeys, self.error_string(None, key, msg + " missing key"))
            if key in fkeys:
                self.assertEqualWrapper(found[key], expected[key], msg + " value")

    def assertReasonablyEqualDictionaryWrapper(self, found, expected, percent, msg):
        fkeys = found.keys()
        for key in expected.keys():
            self.assertTrue(key in fkeys, self.error_string(None, key, msg + " missing key"))
            if key in fkeys:
                self.assertReasonablyEqualWrapper(found[key], expected[key], percent, msg + " value")
