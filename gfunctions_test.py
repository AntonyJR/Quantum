from math import pi
from unittest.mock import Mock
from unittest import main
from test_register import TestRegister

import gfunctions

class TestQuantumHTTP(TestRegister):
    def test_quantum_http(self):
        data = {
                    "num_qbits": 3,
                    "num_measures": 10000,
                    "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
                    "operations": [
                        {"op": 'H', "qbit": 3},
                        {"op": 'P', "qbit": 3, "theta": pi},
                        {"op": 'H', "qbit": 3}
                    ]
                }
        req = Mock()
        req.get_json = Mock(return_value = data)
        req.headers = {'content-type' : 'application/json'}
        res = gfunctions.quantum_http(req)
        self.assertEqualDictionaryWrapper(res["states"], {"|001>": 1.0},
                                          "Phase shift between 2 Hadamard gate same qubit probability")


if __name__ == '__main__':
    main()
