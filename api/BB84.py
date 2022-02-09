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

