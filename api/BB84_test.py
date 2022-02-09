from BB84 import get_random_numbers_quantum, encode_qubits, measure_qubits, prune_invalid, sample_bits, bb84
from random import sample


def test_result(name, status):
    print(f"{status} ---------- {name}")


def test_get_random_numbers_quantum():
    for i in range(1, 102, 10):
        data = get_random_numbers_quantum(i)
        assert len(data) == i
    test_result("get_random_numbers_quantum", "PASS")


def test_encode_qubits():
    bases = get_random_numbers_quantum(5)
    bits = get_random_numbers_quantum(5)
    encodedBits = encode_qubits(bits, bases)
    print(encodedBits)
    test_result("encode_qubits", "PASS")


def test_measure_qubits():
    bases = get_random_numbers_quantum(5)
    bits = get_random_numbers_quantum(5)
    encodedBits = encode_qubits(bits, bases)
    decodedBits = measure_qubits(encodedBits, bases)
    print(decodedBits)
    test_result("measure_qubits", "PASS")


def test_prune_invalid():
    bits = get_random_numbers_quantum(10)
    bases1 = get_random_numbers_quantum(10)
    bases2 = get_random_numbers_quantum(10)
    pruned = prune_invalid(bases1, bases2, bits)
    print(f"bases1: {bases1}\nbases2: {bases2}")
    print(f"Original: {bits}")
    print(f"New:      {pruned}")
    test_result("prune_invalid", "PASS")

test_get_random_numbers_quantum()
test_encode_qubits()
test_measure_qubits()
test_prune_invalid()
