from qiskit import QuantumCircuit, QuantumRegister
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector

# returns a circuit that teleports one qubit state to another location using a helper qubit
def quantum_teleport(nQubits: int, origin: int, destination: int, aux: int):
    qr = QuantumRegister(nQubits)
    # (see comment below — only needed if actually using two quantum computers)
    # cl1 = ClassicalRegister(1)
    # cl2 = ClassicalRegister(1)
    # teleport_qc = QuantumCircuit(qr, cl1, cl2)
    teleport_qc = QuantumCircuit(qr)
    teleport_qc.h(destination)
    teleport_qc.cx(destination, aux)
    teleport_qc.cx(origin, aux)
    teleport_qc.h(origin)
    # (for "true" teleportation with two different quantum computers, you'd measure, but we have to forgo that here)
    # teleport_qc.measure([origin], [0])
    # teleport_qc.measure([aux], [1])
    # teleport_qc.x(destination).c_if(cl2, 1)
    # teleport_qc.z(destination).c_if(cl1, 1)
    teleport_qc.cx(aux, destination)
    teleport_qc.cz(origin, destination)
    return teleport_qc
