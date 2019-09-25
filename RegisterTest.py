from register import Register
from register import ROOT2RECIPRICOL
from math import pi
from math import sqrt


def main():
    simple_register_test(10000)
    cat_states_test(10000)
    full_superposition_test(1000)
    hadamard_gate_test(1000)
    phase_shift_test(10000)


def print_result(register):
    print("after  " + register.vector_as_string())
    print(register.states_as_string())
    print("")


def simple_register_test(num_measures=100):
    # Simple register test
    # test creation of register and measure of state
    print("Simple Register")
    simple_register = Register(3, num_measures)
    simple_register.unit_vector[1] = 1.  # initializes the first state
    print("before " + simple_register.vector_as_string())
    print_result(simple_register)


def full_superposition_test(num_measures=100):
    print("Full Superposition")
    full_register = Register(num_measures=1000)
    full_register.unit_vector = [1. / sqrt(
        full_register.number_of_states)] * full_register.number_of_states  # initializes all states
    print("before " + full_register.vector_as_string())
    print_result(full_register)


def cat_states_test(num_measures=100):
    # Cat states test
    # test creation of register and measure of state
    print("Cat States")
    cat_register = Register(num_measures=num_measures)
    cat_register.unit_vector[0] = ROOT2RECIPRICOL  # initializes the first state
    cat_register.unit_vector[cat_register.number_of_states - 1] = ROOT2RECIPRICOL
    print("before " + cat_register.vector_as_string())
    print_result(cat_register)


def hadamard_gate_test(num_measures=100):
    # Test application of single Hadamand gate
    for i in range(1, 4):
        print("Hadamard Gate " + str(i))
        hadamard = Register(num_measures=num_measures)
        hadamard.unit_vector[0] = 1.
        print("before " + hadamard.vector_as_string())
        hadamard.hadamard_gate(i)
        print_result(hadamard)

    # Test application of multiple Hadamand gate
    print("Hadamard H1 H1 Psi")
    hadamard = Register(num_measures=num_measures)
    hadamard.unit_vector[0] = 1.
    print("before " + hadamard.vector_as_string())
    hadamard.hadamard_gate(1)
    hadamard.hadamard_gate(1)
    print_result(hadamard)

    # Test application of multiple Hadamand gate
    print("Hadamard H3 H2 H1 Psi")
    hadamard = Register(num_measures=num_measures)
    hadamard.unit_vector[0] = 1.
    print("before " + hadamard.vector_as_string())
    hadamard.hadamard_gate(1)
    hadamard.hadamard_gate(2)
    hadamard.hadamard_gate(3)
    print_result(hadamard)


def phase_shift_test(num_measures=100):
    print("Phase Shift 3 QBits Theta = pi H3 P3 H3 Psi (1000 measurements)")
    theta = pi
    phase_shift = Register(num_measures=num_measures)
    phase_shift.unit_vector[0] = 1.
    print("before " + phase_shift.vector_as_string())
    phase_shift.hadamard_gate(3)
    phase_shift.phase_gate(3, theta)
    phase_shift.hadamard_gate(3)
    print_result(phase_shift)

    print("Phase Shift 5 QBits Theta = pi H3 P3 H3 Psi")
    theta = pi
    phase_shift = Register(5, num_measures)
    phase_shift.unit_vector[0] = 1.
    print("before " + phase_shift.vector_as_string())
    phase_shift.hadamard_gate(3)
    phase_shift.phase_gate(3, theta)
    phase_shift.hadamard_gate(3)
    print_result(phase_shift)

    print("Phase Shift 7 Qbits Theta = pi P3 H3 Psi")
    theta = pi
    phase_shift = Register(7, num_measures)
    phase_shift.unit_vector[0] = 1.
    print("before " + phase_shift.vector_as_string())
    phase_shift.hadamard_gate(3)
    phase_shift.phase_gate(3, theta)
    print_result(phase_shift)

    print("Phase Shift 3 Qbits Theta = pi/2 P3 Psi")
    theta = pi / 2
    phase_shift = Register(3, num_measures)
    phase_shift.unit_vector[1] = 1.
    print("before " + phase_shift.vector_as_string())
    phase_shift.phase_gate(3, theta)
    print_result(phase_shift)


if __name__ == '__main__':
    main()
