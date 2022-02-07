from random import randint
from qiskit import QuantumCircuit
from qiskit import Aer, assemble, transpile


sim = Aer.get_backend("aer_simulator")


def getRandomNumbersQuantum(n: int) -> list:
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()
    qobj = assemble(qc, shots=n, memory=True)
    return sim.run(qobj).result().get_memory()


def getRandomNumbersClassical(n: int) -> list:
    return [randint(0, 1) for _ in range(n)]


def encodeQubit():
    # choose random basis (x or z)
    # encode a qubit into superposition of chosen basis
    pass
