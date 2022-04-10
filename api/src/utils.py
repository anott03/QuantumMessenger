from qiskit import QuantumCircuit, assemble

def get_random_numbers(n: int, sim) -> list:
    random_generator_qc = QuantumCircuit(1)
    random_generator_qc.h(0)
    random_generator_qc.measure_all()
    qobj = assemble(random_generator_qc, shots=n, memory=True)
    return [int(item) for item in sim.run(qobj).result().get_memory()]
