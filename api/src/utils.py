from qiskit import QuantumCircuit, assemble

def get_random_numbers(n: int, sim) -> list:
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()
    qobj = assemble(qc, shots=n, memory=True)
    return [int(item) for item in sim.run(qobj).result().get_memory()]
