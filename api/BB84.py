from random import randint, sample
from qiskit import QuantumCircuit
from qiskit import Aer, assemble
from numpy import mod

sim = Aer.get_backend("aer_simulator")


def get_random_numbers_quantum(n: int) -> list:
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()
    qobj = assemble(qc, shots=n, memory=True)
    return sim.run(qobj).result().get_memory()


def getRandomNumbersClassical(n: int) -> list:
    return [randint(0, 1) for _ in range(n)]


def encode_qubits(bits: list, bases: list):
    encodedBits = []
    # choose random basis (x or z)
    # 0 --> X basis
    # 1 --> Z basis
    if not bases:
        bases = get_random_numbers_quantum(len(bits))
    # encode a qubit into superposition of chosen basis
    for bit, base in zip(bits, bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if base == 0:  # X basis
            qc.h(0)
        encodedBits.append(qc)
    return encodedBits


def measure_qubits(bits: list, bases: list):
    meas = []
    for bit, base in zip(bits, bases):
        if base == 0:  # Z basis measurement
            bit.measure(0, 0)
        else:  # X basis measurement
            bit.h(0)  # "rotate" the basis again, since raw measurement can only be done in Z
            bit.measure(0, 0)
        qobj = assemble(bit, shots=1, memory=True)  # Only want one try to mirror real-world situation
        # Run the circuit and fetch the measured bit from the classical register
        meas.append(int(sim.run(qobj).result().get_memory()[0]))
    return meas


def prune_invalid(bases1, bases2, bits):
    # only keep the bits in which bases were the same, so the measurement is assured to be the same
    valid_bits = []
    for base1, base2, bit in zip(bases1, bases2, bits):
        if base1 == base2:  # bit is only valid if its bases were the same
            valid_bits.append(bit)
    return valid_bits


def sample_bits(bits: list, sampleIndices: list):
    # "Publicly" compare a subset of final key to ensure that the protocol worked
    sampled = []
    for i in sampleIndices:
        # Have to calculate i modulo length of bits since we are changing the list length as we go, so we don't access indices out of range
        # We pop the element each time so it gets removed from the bits, since any bits they publicly share should not be part of their final secret key
        sampled.append(bits.pop(mod(i, len(bits))))
    return sampled

