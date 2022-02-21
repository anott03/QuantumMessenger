from random import sample
from qiskit import QuantumCircuit
from qiskit import Aer, assemble
from numpy import mod


class QuantumUtils:
    def get_random_numbers(n: int, sim) -> list:
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.measure_all()
        qobj = assemble(qc, shots=n, memory=True)
        return [int(item) for item in sim.run(qobj).result().get_memory()]

    # Still deciding whether this should be a part of QuantumUtils or if it
    # should go in BB84...
    def prune_invalid(bases1, bases2, bits):
        # only keep the bits in which bases were the same, so the measurement
        # is assured to be the same
        valid_bits = []
        for base1, base2, bit in zip(bases1, bases2, bits):
            if base1 == base2:  # bit is only valid if its bases were the same
                valid_bits.append(bit)
        return valid_bits


class BB84:
    def __init__(self):
        self.sim = Aer.get_backend("aer_simulator")

    def encode_qubits(self, bits: list, bases: list):
        encoded_bits = []
        # choose random basis (x or z)
        # 0 --> Z basis
        # 1 --> X basis
        if not bases:
            bases = QuantumUtils.get_random_numbers(len(bits))
        # encode a qubit into superposition of chosen basis
        for bit, base in zip(bits, bases):
            qc = QuantumCircuit(1, 1)
            if bit == 1:
                qc.x(0)
            if base == 1:  # X basis
                qc.h(0)
            encoded_bits.append(qc)
        return encoded_bits

    def measure_qubits(self, bits: list, bases: list):
        meas = []
        for bit, base in zip(bits, bases):
            if base == 0:  # Z basis measurement
                bit.measure(0, 0)
            else:  # X basis measurement
                # "rotate" the basis again, since raw measurement can only be
                # done in Z
                bit.h(0)
                bit.measure(0, 0)
            # Only want one try to mirror real-world situation
            qobj = assemble(bit, shots=1, memory=True)
            # Run the circuit and fetch the measured bit from the classical
            # register
            meas.append(int(self.sim.run(qobj).result().get_memory()[0]))
        return meas

    def sample_bits(self, bits: list, sample_indices: list):
        # "Publicly" compare a subset of final key to ensure that the protocol
        # worked
        sampled = []
        for i in sample_indices:
            # Have to calculate i modulo length of bits since we are changing
            # the list length as we go, so we don't access indices out of range
            # We pop the element each time so it gets removed from the bits,
            # since any bits they publicly share should not be part of their
            # final secret key
            sampled.append(bits.pop(mod(i, len(bits))))
        return sampled

    # --- Implementing the Protocol ---
    def bb84(self, keyLen: int):
        initial_bits = QuantumUtils.get_random_numbers(
            keyLen, self.sim
        )
        bases1 = QuantumUtils.get_random_numbers(keyLen, self.sim)
        encoded = self.encode_qubits(initial_bits, bases1)
        # * transmit to other person *
        bases2 = QuantumUtils.get_random_numbers(keyLen, self.sim)
        decoded = self.measure_qubits(encoded, bases2)
        pruned1 = QuantumUtils.prune_invalid(bases1, bases2, initial_bits)
        pruned2 = QuantumUtils.prune_invalid(bases1, bases2, decoded)
        sampleIndices = sample(range(len(initial_bits)), keyLen//5)
        sampled1 = self.sample_bits(pruned1, sampleIndices)
        sampled2 = self.sample_bits(pruned2, sampleIndices)
        if sampled1 == sampled2:
            print("Protocol success!")
            return "".join([str(x) for x in decoded])
        else:
            print("Sample mismatch...")
