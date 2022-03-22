from qiskit import QuantumCircuit, QuantumRegister
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector

# returns a circuit that teleports one qubit state to another location using a helper qubit
def quantum_teleport(nQubits: int, origin: int, destination: int, aux: int):
    qr = QuantumRegister(nQubits)
    # (see comment below — only needed if actually using two quantum computers)
    # cl1 = ClassicalRegister(1)
    # cl2 = ClassicalRegister(1)
    # qc = QuantumCircuit(qr, cl1, cl2)
    qc = QuantumCircuit(qr)
    qc.h(destination)
    qc.cx(destination, aux)
    qc.cx(origin, aux)
    qc.h(origin)
    # (for "true" teleportation with two different quantum computers, you'd measure, but we have to forgo that here)
    # qc.measure([origin], [0])
    # qc.measure([aux], [1])
    # qc.x(destination).c_if(cl2, 1)
    # qc.z(destination).c_if(cl1, 1)
    qc.cx(aux, destination)
    qc.cz(origin, destination)
    return qc
