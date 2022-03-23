from random import sample
from qiskit import QuantumCircuit, Aer, assemble, transpile
from qiskit.providers.aer.library.save_instructions import save_statevector
from numpy import mod
import utils
from qTeleportation import quantum_teleport
from qiskit.visualization import plot_bloch_multivector

class BB84:
    def __init__(self):
        self.sim = Aer.get_backend("aer_simulator")

    def encode_qubits(self, bits: list, bases: list):
        encoded_bits = []
        # choose random basis (x or z)
        # 0 --> Z basis
        # 1 --> X basis
        if not bases:
            bases = utils.get_random_numbers(len(bits), self.sim)
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

    @staticmethod
    def prune_invalid(bases1, bases2, bits):
        # only keep the bits in which bases were the same, so the measurement
        # is assured to be the same
        valid_bits = []
        for base1, base2, bit in zip(bases1, bases2, bits):
            if base1 == base2:  # bit is only valid if its bases were the same
                valid_bits.append(bit)
        return valid_bits

    @staticmethod
    def sample_bits(bits: list, sample_indices: list):
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
        initial_bits = utils.get_random_numbers(
            keyLen, self.sim
        )
        bases1 = utils.get_random_numbers(keyLen, self.sim)
        encoded = self.encode_qubits(initial_bits, bases1)
        # * transmit to other person *
        bases2 = utils.get_random_numbers(keyLen, self.sim)
        decoded = self.measure_qubits(encoded, bases2)
        pruned1 = self.prune_invalid(bases1, bases2, initial_bits)
        pruned2 = self.prune_invalid(bases1, bases2, decoded)
        sampleIndices = sample(range(len(initial_bits)), keyLen//5)
        sampled1 = self.sample_bits(pruned1, sampleIndices)
        sampled2 = self.sample_bits(pruned2, sampleIndices)
        if sampled1 == sampled2:
            print("Protocol success!")
            return "".join([str(x) for x in decoded])
        else:
            print("Sample mismatch...")
            return None


class ParallelBB84:
    def __init__(self, key_len):
        self.sim = Aer.get_backend("aer_simulator")
        self.key_len = key_len
        self.masterQC = QuantumCircuit(2 * key_len + 1, key_len)
        self.sender_bases = []
        self.receiver_bases = []

    def reset(self):
        self.masterQC = QuantumCircuit(2 * self.key_len + 1, self.key_len)
        self.sender_bases = []
        self.receiver_bases = []

    # Returns a quantum circuit with N quantum registers
    def encode_qubits(self, bits: list, bases: list):
        print(f"Bits:        {''.join(list(map(str, bits)))}")
        print(f"Alice Bases: {''.join(list(map(str, bases)))}")
        self.sender_bases = bases
        qc = QuantumCircuit(len(bits))
        # choose random basis (0 --> Z basis, 1 --> X basis)
        # encode a qubit into superposition of chosen basis
        i = 0
        for bit, base in zip(bits, bases):
            if bit == 1:
                qc.x(i)
            if base == 1:  # X basis
                qc.h(i)
            i += 1
        return qc

    # Returns a quantum circuit with 2N+1 quantum registers
    def bulk_teleport(self, fromQs: list, toQs: list):
        nQubits = 2*len(fromQs)+1
        qc = QuantumCircuit(nQubits)
        for fromQ, toQ in zip(fromQs, toQs):
            qc.compose(quantum_teleport(nQubits, fromQ, toQ, nQubits-1), qubits=range(nQubits), inplace=True)
            qc.reset(10)
        return qc

    # Returns a quantum circuit with N quantum registers and N classical registers
    def measure_qubits(self, bases: list):
        qc = QuantumCircuit(len(bases), len(bases))
        for i, base in enumerate(bases):
            if base == 0:  # Z basis measurement
                qc.measure(i, i)
            else:  # X basis measurement
                # "rotate" the basis again, since raw measurement can only be done in Z
                qc.h(i)
                qc.measure(i, i)
        return qc

    def sender_protocol(self):
        self.reset()
        self.masterQC.compose(
            self.encode_qubits(
                utils.get_random_numbers(self.key_len, self.sim),
                utils.get_random_numbers(self.key_len, self.sim)
            ),
            qubits=range(self.key_len), inplace=True
        )

        self.masterQC.compose(
            self.bulk_teleport(
                list(range(self.key_len)),
                list(range(self.key_len, 2*self.key_len))
            ),
            qubits=range(2*self.key_len+1), inplace=True
        )
        self.masterQC.save_statevector()
        return self.sim.run(transpile(self.masterQC, self.sim)).result().get_statevector()

    def receiverProtocol(self, state):
        self.masterQC = QuantumCircuit(2*self.key_len+1, self.key_len+2)
        self.masterQC.set_statevector(state)
        self.masterQC.compose(self.measure_qubits(utils.get_random_numbers(self.key_len, self.sim)), qubits=list(range(self.key_len, 2*self.key_len)), clbits=list(range(self.key_len)))
        qobj = assemble(self.masterQC, shots=1, memory=True)
        return self.sim.run(qobj).result().get_memory()
