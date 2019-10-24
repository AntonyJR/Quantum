import cmath
import math
import random
import copy

import numpy

DEFAULT_QBITS = 3
DEFAULT_MEASURES = 100
ROOT2RECIPRICOL = 1 / math.sqrt(2)
I = numpy.array([[1, 0],
                 [0, 1]])
H = ROOT2RECIPRICOL * numpy.array([[1, 1],
                                   [1, -1]])
X = numpy.array([[0, 1],
                 [1, 0]])
Y = numpy.array([[0, complex(0, -1)],
                 [complex(0, 1), 0]])
Z = numpy.array([[1, 0],
                 [0, -1]])


class Register(object):
    def __init__(self, num_qbits=DEFAULT_QBITS, num_measures=DEFAULT_MEASURES):
        self.num_qbits = num_qbits  # number of qbits
        self.number_of_states = 2 ** self.num_qbits
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
        return "|" + format(i, "0" + str(self.num_qbits) + "b") + ">"

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

    def hadamard_gate(self, qbit):
        """
        :param qbit:start AT 1
        :return:
        """
        self.gate_function(qbit, H)

    def phase_gate(self, qbit, theta):
        """
        :param qbit:start AT 1
        :param theta: user defines theta in radians
        :return:
        """
        R = numpy.array([[1, 0],
                         [0, cmath.exp(1j * complex(theta))]])
        self.gate_function(qbit, R)

    def pauli_x_gate(self, qbit):
        """
        :param qbit:start AT 1
        :return:
        """
        self.gate_function(qbit, X)

    def pauli_y_gate(self, qbit):
        """
        :param qbit:start AT 1
        :return:
        """
        self.gate_function(qbit, Y)

    def pauli_z_gate(self, qbit):
        """
        :param qbit:start AT 1
        :return:
        """
        self.gate_function(qbit, Z)

    def gate_function(self, qbit, T):
        exec_sequence = [I] * self.num_qbits
        exec_sequence[qbit - 1] = T
        gate = exec_sequence[0]
        for m in exec_sequence[1:]:
            gate = numpy.kron(gate, m)

        self.unit_vector = numpy.dot(gate, self.unit_vector)
        self.unit_vector = self.unit_vector.tolist()

    def j_gate(self):
        self.unit_vector = numpy.dot(self.J, self.unit_vector)
        self.unit_vector = self.unit_vector.tolist()

    def oracle(self, desired_state):
        o = numpy.identity(self.number_of_states)
        o[desired_state, desired_state] = -1.
        self.unit_vector = numpy.dot(o, self.unit_vector)
        self.unit_vector = self.unit_vector.tolist()

    def repeat(self, count, operations):
        for i in range(count):
            self.execute_operations(operations)

    def execute_operations(self, operations):
        """
        Perform list of operations on register
        :param operations:
             [
                {"op" : 'H', "args" : {"qbit" : 3}},
                {"op" : 'P', "args" : {"qbit" : 3, "theta" : 0.0}}
                {
                    "op" : 'Repeat', "args" : {"count" : 2, "operations" : [
                        {"op" : 'H', "args" : {"qbit" : 3}}
                ]}
              ]
        :param register:
            Quantum register
            The state of this register will be updated by the operations
        :return:
            {
              "final_vector" : [1.0, 0, 0, 0, 0, 0, 0, 0],
              "states" : { "00100":50.0, "00001":50.0}
            }
        """
        for operation in operations:
            op = self.op_table[operation['op']]
            if 'args' in operation:
                args = operation['args']
            else:
                args = {}
            op(self, **args)

    op_table = {
        'H': hadamard_gate,
        'P': phase_gate,
        'X': pauli_x_gate,
        'Y': pauli_y_gate,
        'Z': pauli_z_gate,
        'O': oracle,
        'J': j_gate,
        'Repeat': repeat
    }


def execute(program):
    """
    :param program:
        {
          "num_qbits" : 3,
          "num_measures" : 100,
          "initial_vector" : [1.0, 0, 0, 0, 0, 0, 0, 0],
          "operations" : [
            {"op" : 'H',
             "args" : {"qbit" : 3}},
            {"op" : 'P',
             "args": {"qbit" : 3, "theta" : 0.0}}
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
        register.execute_operations(program['operations'])
    retval = {
        "final_vector": register.unit_vector,
        "states": register.counting_states()
    }
    return retval