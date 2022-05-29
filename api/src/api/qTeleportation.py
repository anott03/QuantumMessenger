from qiskit import QuantumCircuit, QuantumRegister

"""
--- Quantum Teleportation Submodule ---
Submodule of QuantumMessenger that implements a quantum teleportation circuit with the given origin, destination, and
auxiliary qubit. This protocol uses controlled X and Z gates in lieu of "if" instructions because it is being run on
a single quantum computer, instead of between two different computers as would occur in real life, but the idea and
spirit are preserved: the protocol transports the origin's state to the destination with the aid of the auxiliary qubit.
"""

def quantum_teleport(nQubits: int, origin: int, destination: int, aux: int):
    qr = QuantumRegister(nQubits)
    teleport_qc = QuantumCircuit(qr)
    teleport_qc.h(destination)
    teleport_qc.cx(destination, aux)
    teleport_qc.cx(origin, aux)
    teleport_qc.h(origin)
    teleport_qc.cx(aux, destination)
    teleport_qc.cz(origin, destination)
    return teleport_qc
