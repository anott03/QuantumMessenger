from BB84 import BB84, ParallelBB84, QuantumUtils
from qiskit import Aer
from random import sample


class TestBB84:
    @staticmethod
    def test_get_random_numbers_quantum():
        for i in range(1, 102, 10):
            sim = Aer.get_backend("aer_simulator")
            data = QuantumUtils.get_random_numbers(i, sim)
            assert len(data) == i

    @staticmethod
    def test_encode_qubits():
        bb84 = BB84()
        bases = QuantumUtils.get_random_numbers(5, bb84.sim)
        bits = QuantumUtils.get_random_numbers(5, bb84.sim)
        encoded_bits = bb84.encode_qubits(bits, bases)
        assert len(encoded_bits) == len(bits)

    @staticmethod
    def test_measure_qubits():
        bb84 = BB84()
        bits = QuantumUtils.get_random_numbers(10, bb84.sim)
        bases = QuantumUtils.get_random_numbers(10, bb84.sim)
        encoded_bits = bb84.encode_qubits(bits, bases)
        decoded_bits = bb84.measure_qubits(encoded_bits, bases)
        assert len(encoded_bits) == len(decoded_bits)

    # TODO: figure out how to do this test
    @staticmethod
    def test_prune_invalid():
        sim = Aer.get_backend("aer_simulator")
        bits = QuantumUtils.get_random_numbers(10, sim)
        bases1 = QuantumUtils.get_random_numbers(10, sim)
        bases2 = QuantumUtils.get_random_numbers(10, sim)
        pruned = QuantumUtils.prune_invalid(bases1, bases2, bits)
        print(f"bases1: {bases1}\nbases2: {bases2}")
        print(f"Original: {bits}")
        print(f"New:      {pruned}")

    # TODO: figure out how to do this test
    @staticmethod
    def test_sample_bits():
        bb84 = BB84()
        bits = QuantumUtils.get_random_numbers(10, bb84.sim)
        sampleIndices = sample(range(len(bits)), 5)
        sampled = bb84.sample_bits(bits, sampleIndices)
        print(f"Sample: {sampled}")
        print(f"Bits: {bits}")

    @staticmethod
    def test_bb84():
        bb84 = BB84()
        key = bb84.bb84(50)
        assert key is not None

    @staticmethod
    def test_parallel_bb84():
        parallel_bb84 = ParallelBB84(5)
        post_sender_state = parallel_bb84.sender_protocol()
        results = parallel_bb84.receiver_protocol(post_sender_state)
        print(f"Shared key: {results}")

