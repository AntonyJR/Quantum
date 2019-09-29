import cmath
import math
import random

import numpy

DEFAULT_QBITS = 3
DEFAULT_MEASURES = 100
ROOT2RECIPRICOL = 1 / math.sqrt(2)
I = numpy.array([[1, 0],
                 [0, 1]])
H = ROOT2RECIPRICOL * numpy.array([[1, 1],
                                   [1, -1]])


class Register(object):
    def __init__(self, num_qubits=DEFAULT_QBITS, num_measures=DEFAULT_MEASURES):
        self.num_qubits = num_qubits  # number of qubits
        self.number_of_states = 2 ** self.num_qubits
        self.unit_vector = [0j] * self.number_of_states
        self.numMeasures = num_measures
        self.J = numpy.identity(self.number_of_states)
        self.J[0, 0] = -1.

    def vector_as_string(self):
        return "[" + ", ".join(
            str(round(val.real, 2)) + (format(round(val.imag, 2), "+") + "j" if val.imag * val.imag > 0.0001 else "")
            for val in self.unit_vector) + "]"

    def measure(self):
        q = 0
        measure = random.random()
        for i in range(self.number_of_states):
            q += (self.unit_vector[i].conjugate() * self.unit_vector[i]).real
            if measure < q:
                break
        return "|" + format(i, "0" + str(self.num_qubits) + "b") + ">"

    def counting_states(self):
        state_count = {}
        for i in range(self.numMeasures):
            m = self.measure()
            if m in state_count:
                state_count[m] += 1.0
            else:
                state_count[m] = 1.0
        for state in state_count.keys():
            state_count[state] /= self.numMeasures
        return state_count

    def states_as_string(self):
        states = self.counting_states()
        return "[" + ", ".join(
            state + ":" + str(states[state] * 100.0) + "%" for state in sorted(states.keys())) + \
               "]"

    def hadamard_gate(self, qubit):
        """
        :param qubit:stART AT 1
        :return:
        """
        self.gate_function(qubit, H)

    def phase_gate(self, qubit, theta):
        """
        :param qubit:stART AT 1
        :param theta: user defines theta in radians
        :return:
        """
        R = numpy.array([[1, 0],
                         [0, cmath.exp(1j * complex(theta))]])
        self.gate_function(qubit, R)

    def gate_function(self, qubit, T):
        exec_sequence = [I] * self.num_qubits
        exec_sequence[qubit - 1] = T
        gate = exec_sequence[0]
        for m in exec_sequence[1:]:
            gate = numpy.kron(gate, m)
        self.unit_vector = numpy.dot(gate, self.unit_vector)
        self.unit_vector = self.unit_vector.tolist()

    def j_gate(self):
        self.unit_vector = numpy.dot(self.J, self.unit_vector)
        self.unit_vector = self.unit_vector.tolist()

    def oracle(self, desired_state):
        oracle = numpy.identity(self.number_of_states)
        oracle[desired_state, desired_state] = -1.
        self.unit_vector = numpy.dot(oracle, self.unit_vector)
        self.unit_vector = self.unit_vector.tolist()


def execute(program):
    """
    :param program:
        {
          "num_qbits" : 3,
          "num_measures" : 100,
          "initial_vector" : [1.0, 0, 0, 0, 0, 0, 0, 0],
          "operations" : [
            {"op" : 'H', "qbit" : 3},
            {"op" : 'P', "qbit" : 3, "theta" : 0.0}
          ]
        }
    :return:
        {
          "final_vector" : [1.0, 0, 0, 0, 0, 0, 0, 0],
          "states" : { "00100":50.0, "00001":50.0}
        }

    """
    num_qbits = program['num_qbits'] if 'num_qbits' in program else DEFAULT_QBITS
    num_measures = program['num_measures'] if 'num_measures' in program else DEFAULT_MEASURES
    register = Register(num_qbits, num_measures)
    register.unit_vector = program['initial_vector']
    if "operations" in program:
        for operation in program['operations']:
            if operation['op'] == 'H':
                register.hadamard_gate(operation['qbit'])
            elif operation['op'] == 'P':
                register.phase_gate(operation['qbit'], operation['theta'])
            else:
                pass
    retval = {}
    retval["final_vector"] = register.unit_vector
    retval["states"] = register.counting_states()
    return retval
