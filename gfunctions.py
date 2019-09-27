from flask import jsonify
from register import Register


def quantum_http(request):
    """HTTP Cloud Function.
        Args:
            request (flask.Request): The request object.
            <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
            This should be a json document
            {
              "num_qbits" : 3,
              "num_measures" : 100,
              "initial_vector" : [1.0, 0, 0, 0, 0, 0, 0, 0],
              "operations" : [
                {"op" : 'H', "qbit" : 3},
                {"op" : 'P', "qbit" : 3, "theta" : 0.0}
              ]
            }
        Returns:
            The response text, or any set of values that can be turned into a
            Response object using `make_response`
            <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
            This is a json document
            {
              "final_vector" : [1.0, 0, 0, 0, 0, 0, 0, 0],
              "states" : { "00100":50.0, "00001":50.0}
            }
        """
    content_type = request.headers['content-type']
    if content_type != 'application/json':
        raise ValueError("Unknown content type: {}".format(content_type))
    request_json = request.get_json(silent=True)
    retval = {}
    if request_json:
        register = Register(request_json['num_qbits'], request_json['num_measures'])
        register.unit_vector = request_json['initial_vector']
        for operation in request_json['operations']:
            if operation['op'] == 'H':
                register.hadamard_gate(operation['qbit'])
            elif operation['op'] == 'P':
                register.phase_gate(operation['qbit'], operation['theta'])
            else:
                pass
        retval["final_vector"] = register.vector_as_string()
        retval["states"] = register.counting_states()
    return jsonify(retval)
