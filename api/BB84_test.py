from BB84 import get_random_numbers_quantum, encode_qubits


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


test_get_random_numbers_quantum()
test_encode_qubits()
