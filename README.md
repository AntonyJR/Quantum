# Quantum Computer Gates

This is a Python implementation of the exercises suggested in the paper [Undergraduate computational physics projects on quantum computing][Candela1] (Can1)
The original code was written by my son James Hurford-Reynolds.
I have refactored his code to make it easier to reuse.

## Explanation of Project
The following modules are part of the project:

|**Module**|**Purpose**|
|-------:|:----------|
|[register]|Implementation of Qubits as a quantum register and quantum gates and oeprators.
|[test_register]|Pyunit tests for register.|
|[main]|Google serverless function to run quantum program.|

## Quantum Program Format
The *execute* function in the [register] module and the quantum_http function in the [main] module
both have the same interface of receivng a JSON program description and returning a JSON response.

### Request Format ###
The input json document has the following format
```json
{
  "num_qbits" : 3,
  "num_measures" : 100,
  "initial_vector" : [1.0, 0, 0, 0, 0, 0, 0, 0],
  "operations" : [
    { "op" : 'H', "qbit" : 3},
    { "op" : 'P', "qbit" : 3, "theta" : 0.0},
    { "op" : 'Repeat', "count" : 2,
      "operations" : [
        {"op" : 'H', "qbit" : 1}
      ]
    }
  ]
}
````
* **num_qbits** is the number of Qubits in the register.
* **num_measures** is the number of measurements to take at the end of the program.
* **initial_vector** is the initial input vector and should be 2<SUP>num_qbits</SUP> long
* **operations** is the sequence of gates and operations to apply to the input.
  * Apply Hadamard Gate
    * **op** *H*
    * **qbit** Qubit to apply to
  * Apply Phase Shift gate
    * **op** *P*
    * **qbit** Qubit to apply to
    * **theta** Phase shift in radians
  * Repeat operations
    * **op** *Repeat*
    * **count** Number of times to repeat operations
    * **operations** Operations to apply
  
### Response Format ###
The output json document has the following format
```json
{
  "final_vector" : [1.0, 0, 0, 0, 0, 0, 0, 0],
  "states" : { "|00100>":50.0, "|00001>":50.0}
}
```
* **final_vector** out register values
* **states** result of sampling output vector

Can1: [Undergraduate computational physics projects on quantum computing][Candela1] : D. Candela :
American Journal of Physics 83, 688 (2015); doi: 10.1119/1.4922296

[Candela1]:  https://doi.org/10.1119/1.4922296
[register]: register.py
[test_register]: test_register.py
[main]: main.py