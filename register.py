import cmath
import math
import random

import numpy

ROOT2RECIPRICOL = 1 / math.sqrt(2)
I = numpy.array([[1, 0],
                 [0, 1]])
H = ROOT2RECIPRICOL * numpy.array([[1, 1],
                                   [1, -1]])


class Register(object):
    def __init__(self, num_qubits=3, num_measures=100):
        self.num_qubits = num_qubits  # number of qubits
        self.number_of_states = 2 ** self.num_qubits
        self.unit_vector = [0j] * self.number_of_states
        self.numMeasures = num_measures

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
