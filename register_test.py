from math import pi
from math import sqrt
from unittest import TestCase
from unittest import main

from register import ROOT2RECIPRICOL
from register import Register
from register import execute


# Tests based on exercises in "Undergraduate computational physics projects on quantum computing" D. Candela
# Citation: American Journal of Physics 83, 688 (2015); doi: 10.1119/1.4922296
# View online: https://doi.org/10.1119/1.4922296
# View Table of Contents: https://aapt.scitation.org/toc/ajp/83/8
# Published by the American Association of Physics Teachers

class TestRegister(TestCase):
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
        tolerance = complex(percent, percent)
        self.assertTrue(abs(delta.real) <= tolerance.real and abs(delta.imag) <= tolerance.imag,
                        self.error_string(found, expected, msg))

    def assertSequenceEqualWrapper(self, found, expected, msg):
        self.assertSequenceEqual(found, expected,
                                 self.error_string(found, expected, msg))

    def assertReasonablyEqualSequenceWrapper(self, found, expected, percent, msg):
        self.assertEqualWrapper(len(found), len(expected), msg + " length")
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
        self.assertEqualWrapper(len(found), len(expected), msg + " length")
        fkeys = found.keys()
        for key in expected.keys():
            self.assertTrue(key in fkeys, self.error_string(None, key, msg + " missing key"))
            if key in fkeys:
                self.assertReasonablyEqualWrapper(found[key], expected[key], percent, msg + " value")

    def test_simple_register_create(self, ):
        # Programming project 1
        # Simple register test
        # test creation of register
        num_qbits = 3
        simple_register = Register(num_qbits, self.num_measures)
        self.assertEqualWrapper(num_qbits, simple_register.num_qubits, "Wrong number of qbits")
        self.assertEqualWrapper(self.num_measures, simple_register.numMeasures, "Wrong number of measures")
        self.assertEqualWrapper(2 ** num_qbits, simple_register.number_of_states, "Wrong number of states")
        self.assertSequenceEqualWrapper(simple_register.unit_vector, [0.0] * 2 ** num_qbits,
                                        "Incorrect initial unit vector")

    def test_simple_register_states(self, ):
        # Programming project 1
        # Simple register test
        # test measure of simple states
        num_qbits = 3
        simple_register = Register(num_qbits, self.num_measures)
        # Set the initial state |W> to one of the basis states, for example, |011> [Eq. (6)].
        # With this initial state, every measurement should give the result |011>.
        for i in range(simple_register.number_of_states):
            # Test measurement of each single state
            if i > 0:
                simple_register.unit_vector[i - 1] = 0.0
            simple_register.unit_vector[i] = 1.0
            states = simple_register.counting_states()
            self.assertEqualDictionaryWrapper(states, {self.make_state_string(i, num_qbits): 1.0},
                                              "Invalid state measurement")

    def test_cat_states(self):
        # Programming project 1
        # Cat states test
        # Set the initial state to the cat state, Eq. (7).
        # Now, at random, either all of the qubits should be 0 or all of the qubits should be 1
        num_qbits = 3
        cat_register = Register(num_qubits=num_qbits, num_measures=self.num_measures)
        cat_register.unit_vector[0] = ROOT2RECIPRICOL  # initializes the first state
        cat_register.unit_vector[cat_register.number_of_states - 1] = ROOT2RECIPRICOL
        states = cat_register.counting_states()
        test_states = {"|000>": 0.50, "|111>": 0.50}
        self.assertReasonablyEqualDictionaryWrapper(states, test_states, self.state_accuracy_percent,
                                                    "Incorrect cat state")

    def test_full_superposition(self):
        # Programming project 1
        # Test all states equally likely
        # Set the initial state to an equal superposition of all 2N basis states,
        # With this state the measured value for each qubit is both random and uncorrelated with the other qubits.
        # Thus, all possible results from j000i to j111i should occur, each with equal frequency to within
        # statistical fluctuations.
        num_qbits = 3
        full_register = Register(num_qubits=num_qbits, num_measures=self.num_measures)
        full_register.unit_vector = [1. / sqrt(
            full_register.number_of_states)] * full_register.number_of_states  # initializes all states
        probabilities = full_register.counting_states()
        expected_prob = 1.0 / full_register.number_of_states
        for probability in probabilities.values():
            self.assertReasonablyEqualWrapper(probability, expected_prob, self.state_accuracy_percent,
                                              "Bad probability")

    def test_hadamard_gate_single(self):
        # Programming project 2

        # Test application of single Hadamard gate
        #  A Hadamard gate is applied to qubit 2.
        #  From Eq. (14), this puts qubit 2 in an equal superposition |0> and |1>.
        #  Therefore, the result of the calculation should vary randomly between the two possibilities, |000> and |010>.
        num_qbits = 3
        test_vector = [
            None,
            [ROOT2RECIPRICOL, 0.0, 0.0, 0.0, ROOT2RECIPRICOL, 0.0, 0.0, 0.0],
            [ROOT2RECIPRICOL, 0.0, ROOT2RECIPRICOL, 0.0, 0.0, 0.0, 0.0, 0.0],
            [ROOT2RECIPRICOL, ROOT2RECIPRICOL, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        test_states = [
            None,
            {"|000>": 0.5, "|100>": 0.5},
            {"|000>": 0.5, "|010>": 0.5},
            {"|000>": 0.5, "|001>": 0.5}
        ]
        for i in range(1, num_qbits + 1):
            hadamard = Register(num_qubits=num_qbits, num_measures=self.num_measures)
            hadamard.unit_vector[0] = 1.
            hadamard.hadamard_gate(i)
            states = hadamard.counting_states()
            self.assertEqualWrapper(hadamard.unit_vector, test_vector[i],
                                    "Incorrect unit vector after Hadamard " + str(i))
            self.assertReasonablyEqualDictionaryWrapper(states, test_states[i], self.state_accuracy_percent,
                                                        "Incorrect single Hadamard gate probability")

    def test_pauli_x_gate_single(self):
        # Test application of single Pauli X (NOT) gate
        num_qbits = 3
        test_vector = [
            None,
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        test_states = [
            None,
            {"|100>": 1.0},
            {"|010>": 1.0},
            {"|001>": 1.0}
        ]
        for i in range(1, num_qbits + 1):
            paulix = Register(num_qubits=num_qbits, num_measures=self.num_measures)
            paulix.unit_vector[0] = 1.
            paulix.pauli_x_gate(i)
            states = paulix.counting_states()
            self.assertEqualWrapper(paulix.unit_vector, test_vector[i],
                                    "Incorrect unit vector after Pauli X " + str(i))
            self.assertReasonablyEqualDictionaryWrapper(states, test_states[i], self.state_accuracy_percent,
                                                        "Incorrect single Pauli X gate probability")
    def test_pauli_y_gate_single(self):
        # Test application of single Pauli X (NOT) gate
        num_qbits = 3
        test_vector = [
            None,
            [0.0, 0.0, 0.0, 0.0, complex(0.0, 1.0), 0.0, 0.0, 0.0],
            [0.0, 0.0, complex(0.0, 1.0), 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, complex(0.0, 1.0), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        test_states = [
            None,
            {"|100>": 1.0},
            {"|010>": 1.0},
            {"|001>": 1.0}
        ]
        for i in range(1, num_qbits + 1):
            pauliy = Register(num_qubits=num_qbits, num_measures=self.num_measures)
            pauliy.unit_vector[0] = 1.
            pauliy.pauli_y_gate(i)
            states = pauliy.counting_states()
            self.assertEqualWrapper(pauliy.unit_vector, test_vector[i],
                                    "Incorrect unit vector after Pauli Y " + str(i))
            self.assertReasonablyEqualDictionaryWrapper(states, test_states[i], self.state_accuracy_percent,
                                                        "Incorrect single Pauli X gate probability")
    def test_pauli_z_gate_single(self):
        # Test application of single Pauli X (NOT) gate
        num_qbits = 3
        test_vector = [
            None,
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        test_states = [
            None,
            {"|001>": 1.0},
            {"|001>": 1.0},
            {"|001>": 1.0}
        ]
        for i in range(1, num_qbits + 1):
            pauliz = Register(num_qubits=num_qbits, num_measures=self.num_measures)
            pauliz.unit_vector[1] = 1.
            pauliz.pauli_z_gate(i)
            states = pauliz.counting_states()
            self.assertEqualWrapper(pauliz.unit_vector, test_vector[i],
                                    "Incorrect unit vector after Pauli X " + str(i))
            self.assertReasonablyEqualDictionaryWrapper(states, test_states[i], self.state_accuracy_percent,
                                                        "Incorrect single Pauli X gate probability")



    def test_execute_no_op(self):
        # Test execute function correctly reads input
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [0, 1., 0, 0, 0, 0, 0, 0],
            "operations": [
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|001>": 1.0},
                                          "Incorrect no op execute")

    def test_execute_missing_operations(self):
        # Test execute function handles missing operations
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [0, 1., 0, 0, 0, 0, 0, 0],
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|001>": 1.0},
                                          "Incorrect missing operations execute")

    def test_execute_missing_measures(self):
        # Test execute function handles missing num measures
        request = {
            "num_qbits": 3,
            "initial_vector": [0, 1., 0, 0, 0, 0, 0, 0],
            "operations": [
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|001>": 1.0},
                                          "Incorrect missing measures execute")

    def test_execute_missing_qbits(self):
        # Test execute function handles missing num qbits
        request = {
            "num_measures": self.num_measures,
            "initial_vector": [0, 1., 0, 0, 0, 0, 0, 0],
            "operations": [
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|001>": 1.0},
                                          "Incorrect missing num qbits execute")

    def test_hadamard_gate_all_qbits(self):
        # Programming project 2

        # In Fig. 3(b), Hadamard gates are applied to qubits 1, 2, and 3.
        # This leaves each of the three qubits equally likely to be in the states |0> and |1>,
        # with no correlations between the qubits.
        # Knowing the state of qubit 1, for example, gives no information about the states of qubits 2 and 3
        # The result of the calculation should vary randomly between all eight possibilities, |000>; |001>; ...; |111>.
        num_qbits = 3
        num_states = 2 ** num_qbits
        request = {
            "num_qbits": num_qbits,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {"op": 'H', "qbit": 1},
                {"op": 'H', "qbit": 2},
                {"op": 'H', "qbit": 3}
            ]
        }
        result = execute(request)
        expected_states = {}
        for j in range(0, num_states):
            expected_states[self.make_state_string(j, num_qbits)] = 1 / num_states
        self.assertReasonablyEqualDictionaryWrapper(result["states"], expected_states, self.state_accuracy_percent,
                                                    "Incorrect Hadamard gate applied to each qubit probability")

    def test_hadamard_gate_all_qbits_nested(self):
        # As previous test except this time it is a nested call with a single repeat
        # Programming project 2

        # In Fig. 3(b), Hadamard gates are applied to qubits 1, 2, and 3.
        # This leaves each of the three qubits equally likely to be in the states |0> and |1>,
        # with no correlations between the qubits.
        # Knowing the state of qubit 1, for example, gives no information about the states of qubits 2 and 3
        # The result of the calculation should vary randomly between all eight possibilities, |000>; |001>; ...; |111>.
        num_qbits = 3
        num_states = 2 ** num_qbits
        request = {
            "num_qbits": num_qbits,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {
                    "op": 'Repeat', "count": 1,
                    "operations": [
                        {"op": 'H', "qbit": 1},
                        {"op": 'H', "qbit": 2},
                        {"op": 'H', "qbit": 3}
                    ]
                }
            ]
        }
        result = execute(request)
        expected_states = {}
        for j in range(0, num_states):
            expected_states[self.make_state_string(j, num_qbits)] = 1 / num_states
        self.assertReasonablyEqualDictionaryWrapper(result["states"], expected_states, self.state_accuracy_percent,
                                                    "Incorrect Hadamard gate applied to each qubit probability")

    def test_hadamard_gate_H1_H1(self):
        # Programming project 2

        # Test application of multiple Hadamand gate
        # In Fig. 3(c), two successive Hadamard gates are applied to the same qubit.
        # As shown above, the Hadamard gate splits a single quantum amplitude into two but
        # it can also put two quantum amplitudes back together into one.
        # In this case, the second Hadamard undoes the effect of the first one,
        # so the result of the calculation should always be |000>.
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {"op": 'H', "qbit": 1},
                {"op": 'H', "qbit": 1}
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|000>": 1.0},
                                          "Incorrect 2 Hadamard gate same qubit probability")

    def test_hadamard_gate_H1_H1_repeat(self):
        # As previous test except this time it is a nested call with two repeats
        # Programming project 2

        # Test application of multiple Hadamand gate
        # In Fig. 3(c), two successive Hadamard gates are applied to the same qubit.
        # As shown above, the Hadamard gate splits a single quantum amplitude into two but
        # it can also put two quantum amplitudes back together into one.
        # In this case, the second Hadamard undoes the effect of the first one,
        # so the result of the calculation should always be |000>.
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {
                    "op": 'Repeat', "count": 2,
                    "operations": [
                        {"op": 'H', "qbit": 1}
                    ]
                }
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|000>": 1.0},
                                          "Incorrect 2 Hadamard gate same qubit probability")

    def test_pauli_x_gate_X3(self):
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {"op": 'X', "qbit": 3}
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|001>": 1.0},
                                          "Incorrect X gate qubit probability")

    def test_pauli_x_gate_X3_X3(self):
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {
                    "op": 'Repeat', "count": 2,
                    "operations": [
                        {"op": 'X', "qbit": 3}
                    ]
                }
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|000>": 1.0},
                                          "Incorrect X gate qubit probability")

    def test_pauli_y_gate_Y3(self):
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {"op": 'Y', "qbit": 3}
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|001>": 1.0},
                                          "Incorrect Y gate qubit probability")
        self.assertEqualWrapper(result["final_vector"], [0.0, complex(0.0, 1.0), 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0],
                                          "Incorrect Y vector")

    def test_pauli_x_gate_Y3_Y3(self):
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {
                    "op": 'Repeat', "count": 2,
                    "operations": [
                        {"op": 'Y', "qbit": 3}
                    ]
                }
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|000>": 1.0},
                                          "Incorrect Y gate qubit probability")

    def test_pauli_z_gate_Z3(self):
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {"op": 'Z', "qbit": 3}
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|000>": 1.0},
                                          "Incorrect Z gate qubit probability")
        self.assertEqualWrapper(result["final_vector"], [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0],
                                          "Incorrect Z vector")

    def test_pauli_z_gate_Z3_Set(self):
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [0.0, 1.0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {"op": 'Z', "qbit": 3}
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|001>": 1.0},
                                          "Incorrect Z gate qubit probability")
        self.assertEqualWrapper(result["final_vector"], [0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0],
                                          "Incorrect Z vector")

    def test_pauli_z_gate_Z3_Z3(self):
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {
                    "op": 'Repeat', "count": 2,
                    "operations": [
                        {"op": 'Z', "qbit": 3}
                    ]
                }
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|000>": 1.0},
                                          "Incorrect Z gate qubit probability")

    def test_pauli_z_gate_Z3_Z3_set(self):
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [0.0, 1.0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {
                    "op": 'Repeat', "count": 2,
                    "operations": [
                        {"op": 'Z', "qbit": 3}
                    ]
                }
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|001>": 1.0},
                                          "Incorrect Z gate qubit probability")

    def test_phase_shift_H3_P3_H3(self):
        # Programming project 2

        # In Fig. 3(d), again two Hadamard gates are applied to the same qubit.
        # But now the phase-shift gate R0 with theta = pi is applied between the two Hadamard gates,
        # shown by a box with p in it.
        # As in the previous case, the result of the calculation is perfectly definite,
        # but now the result is always j001i.
        # The net effect of the three gates has been to flip qubit 3 from |0> to |1>.
        request = {
            "num_qbits": 3,
            "num_measures": self.num_measures,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {"op": 'H', "qbit": 3},
                {"op": 'P', "qbit": 3, "theta": pi},
                {"op": 'H', "qbit": 3}
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|001>": 1.0},
                                          "Phase shift between 2 Hadamard gate same qubit probability")

    def test_phase_shift_5_H3_P3_H3(self):
        # Programming project 2

        # Repeat previous test with 5 qubits
        # Phase Shift 5 QBits Theta = pi H3 P3 H3 Psi
        num_qbits = 5
        num_states = 2 ** num_qbits
        initial = [0.0] * num_states
        initial[0] = 1.0
        request = {
            "num_qbits": num_qbits,
            "num_measures": self.num_measures,
            "initial_vector": initial,
            "operations": [
                {"op": 'H', "qbit": 3},
                {"op": 'P', "qbit": 3, "theta": pi},
                {"op": 'H', "qbit": 3}
            ]
        }
        result = execute(request)
        self.assertEqualDictionaryWrapper(result["states"], {"|00100>": 1.0},
                                          "Phase shift between 2 Hadamard gate same qubit in 5 qubits probability")

    def test_phase_shift_7_P3_H3(self):
        # Programming project 2

        # Repeat previous test with 7 qubits
        # Phase Shift 7 QBits Theta = pi P3 H3 Psi
        num_qbits = 7
        num_states = 2 ** num_qbits
        initial = [0.0] * num_states
        initial[0] = 1.0
        request = {
            "num_qbits": num_qbits,
            "num_measures": self.num_measures,
            "initial_vector": initial,
            "operations": [
                {"op": 'H', "qbit": 3},
                {"op": 'P', "qbit": 3, "theta": pi}
            ]
        }
        result = execute(request)
        self.assertReasonablyEqualDictionaryWrapper(result["states"],
                                                    {"|0000000>": .5, "|0010000>": .5}, self.state_accuracy_percent,
                                                    "Phase shift then Hadamard gate same qubit in 7 qubits probability")

    def test_phase_shift_3_pi2_P3_H3(self):
        # Programming project 2

        # Repeat previous test with 3 qubits
        # Phase Shift 3 QBits Theta = pi/2 P3 H3 Psi
        num_qbits = 3
        theta = pi / 2
        phase_shift = Register(num_qbits, self.num_measures)
        phase_shift.unit_vector[1] = 1.
        phase_shift.phase_gate(3, theta)
        states = phase_shift.counting_states()
        self.assertEqualDictionaryWrapper(states, {"|001>": 1.},
                                          "Phase shift half pi then Hadamard gate same qubit in 3 qubits probability")


if __name__ == '__main__':
    main()
