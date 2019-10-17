from math import pi
from unittest import main, TestCase
from unittest.mock import Mock, patch
from mock_extension import MockExtension

from register_test import TestRegister

from main import quantum_http


def side_effect(json):
    return json


class TestQuantumHTTP(MockExtension):


    @patch('main.jsonify', side_effect=side_effect)
    def test_quantum_http(self, mock_jsonify):
        data = {
            "num_qbits": 3,
            "num_measures": 10000,
            "initial_vector": [1.0, 0, 0, 0, 0, 0, 0, 0],
            "operations": [
                {"op": 'H', "args" : {"qbit": 3}},
                {"op": 'P', "args" : {"qbit": 3, "theta": pi}},
                {"op": 'H', "args" : {"qbit": 3}}
            ]
        }
        req = Mock()
        req.get_json = Mock(return_value=data)
        req.headers = {'content-type': 'application/json'}
        res = quantum_http(req)
        self.assertEqualDictionaryWrapper(res["states"], {"|001>": 1.0},
                                          "Phase shift between 2 Hadamard gate same qubit probability")


if __name__ == '__main__':
    main()
