# Quantum Computer Gates

This is a Python implementation of the exercises suggested in the paper [Undergraduate computational physics projects on quantum computing][Candela1] (Can1)
The original code was written by my son James Hurford-Reynolds.
I have refactored his code to make it easier to reuse.

## Explanation of Project
The following files are part of the project:

|**File**|**Purpose**|
|-------:|:----------|
|[register.py][register]|Implementation of Qubits as a quantum register and quantum gates and oeprators.
|[test_register.py][test_register]|Pyunit tests for register.|
|[main.py][main]|Google serverless function to run quantum program.|

Can1: [Undergraduate computational physics projects on quantum computing][Candela1] : D. Candela :  American Journal of Physics 83, 688 (2015); doi: 10.1119/1.4922296

[Candela1]:  https://doi.org/10.1119/1.4922296
[register]: register.py
[test_register]: test_register.py
[main]: main.py