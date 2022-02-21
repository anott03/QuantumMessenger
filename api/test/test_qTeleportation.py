from qTeleportation import quantum_teleport


class TestQTeleportation:
    # TODO: rethink this test?
    # right now it passes simply by virtue of not throwing any errors
    def test_teleportation(x):
        print("== Circuit 1: 3 qubits, teleport from 1 to 2 with 3 ==")
        print(quantum_teleport(3, 0, 1, 2))
        print("== Circuit 2: 8 qubits, teleport from 3 to 7 with 5 ==")
        print(quantum_teleport(8, 2, 6, 4))
