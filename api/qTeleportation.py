from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def quantumTeleport(nQubits: int, origin: int, destination: int, aux: int):
    # returns a circuit that teleports one qubit state to another location using a helper qubit
    qr = QuantumRegister(nQubits)
    cl1 = ClassicalRegister(1)
    cl2 = ClassicalRegister(1)
    qc = QuantumCircuit(qr, cl1, cl2)
    qc.h(destination)
    qc.cx(destination, aux)
    qc.cx(origin, aux)
    qc.h(origin)
    qc.measure([0], [0])
    qc.measure([1], [1])
    qc.x(2).c_if(cl2, 1)
    qc.z(2).c_if(cl1, 1)
    return qc
