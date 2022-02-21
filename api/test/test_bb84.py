from BB84 import BB84, QuantumUtils
from qiskit import Aer
# from random import sample


class TestBB84:
    def test_get_random_numbers_quantum(x):
        for i in range(1, 102, 10):
            sim = Aer.get_backend("aer_simulator")
            data = QuantumUtils.get_random_numbers(i, sim)
            assert len(data) == i

    def test_encode_qubits(x):
        bb84 = BB84()
        bases = QuantumUtils.get_random_numbers(5, bb84.sim)
        bits = QuantumUtils.get_random_numbers(5, bb84.sim)
        encoded_bits = bb84.encode_qubits(bits, bases)
        assert len(encoded_bits) == len(bits)

    def test_measure_qubits(x):
        bb84 = BB84()
        bits = QuantumUtils.get_random_numbers(10, bb84.sim)
        bases = QuantumUtils.get_random_numbers(10, bb84.sim)
        encoded_bits = bb84.encode_qubits(bits, bases)
        decoded_bits = bb84.measure_qubits(encoded_bits, bases)
        assert len(encoded_bits) == len(decoded_bits)

    # TODO: figure out how to do this test
    #  def test_prune_invalid():
        #  bits = get_random_numbers_quantum(10)
        #  bases1 = get_random_numbers_quantum(10)
        #  bases2 = get_random_numbers_quantum(10)
        #  pruned = prune_invalid(bases1, bases2, bits)
        #  print(f"bases1: {bases1}\nbases2: {bases2}")
        #  print(f"Original: {bits}")
        #  print(f"New:      {pruned}")

    # TODO: figure out how to do this test
    #  def test_sample_bits():
        #  bits = get_random_numbers_quantum(10)
        #  sampleIndices = sample(range(len(bits)), 5)
        #  sampled = sample_bits(bits, sampleIndices)
        #  print(f"Sample: {sampled}")
        #  print(f"Bits: {bits}")

    def test_bb84(x):
        bb84 = BB84()
        key = bb84.bb84(50)
        assert key is not None
