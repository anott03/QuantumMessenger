from random import randint
from qiskit import QuantumCircuit
from qiskit import Aer, assemble, transpile


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
    # 1 --> Z bassi
    if not bases:
        bases = get_random_numbers_quantum(len(bits))
    # encode a qubit into superposition of chosen basis
    for bit, base in zip(bits, bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if base == 0:  # X basis
            qc.h(0)
        qc.barrier()  # not sure if we need this here...
        encodedBits.append(qc)
    return encodedBits
