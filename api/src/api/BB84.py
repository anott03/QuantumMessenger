from qiskit import QuantumCircuit, Aer, assemble, transpile
from qiskit.providers.aer.library.save_instructions import save_statevector
import utils
from qTeleportation import quantum_teleport

"""
--- BB84 Protocol Submodule ---
Submodule of QuantumMessenger that implements the BB84 protocol for quantum key generation. This version runs all steps
on the same quantum computer, not on different ones as would happen in real life, due to limitations of the simulation
environment. However, the idea is still the same: through encoding classical bits as quantum information, transporting
it, and decoding it at the other end, BB84 generates a shared key that can't be intercepted without risking detection.
"""

class ParallelBB84:
    def __init__(self, key_len):
        self.sim = Aer.get_backend("aer_simulator")
        self.key_len = key_len
        self.masterQC = QuantumCircuit(2 * key_len + 1, key_len)
        self.sender_bases = []
        self.receiver_bases = []

    # reset all qubits, including teleportation auxiliary qubits and measurement bits
    # prepares the class to run another instance of the protocol
    def reset(self):
        self.masterQC = QuantumCircuit(2 * self.key_len + 1, self.key_len)
        self.sender_bases = []
        self.receiver_bases = []

    # Portion of protocol that encodes a message comprised of classical bits into qubits, then placing each in a given
    # basis (Z or X) to "secure" the quantum information and eventually catch interceptions
    # Returns a quantum circuit with `key_len` quantum registers
    def encode_qubits(self, bits: list, bases: list):
        self.sender_bases = bases
        encoder_qc = QuantumCircuit(len(bits))
        current_qubit = 0
        for bit, base in zip(bits, bases):
            if bit == 1:
                encoder_qc.x(current_qubit)
            if base == 1:  # X basis
                encoder_qc.h(current_qubit)
            current_qubit += 1
        return encoder_qc

    # Portion of protocol that "transfers" qubits from sender to receiver (real life transportation substituted here
    # for quantum teleportation); sequentially teleports each of the origin qubits to each of the destinations
    # Returns a quantum circuit with 2*`key_len`+1 quantum registers
    def bulk_teleport(self, fromQs: list, toQs: list):
        circuit_span = 2*len(fromQs)+1
        teleport_qc = QuantumCircuit(circuit_span)
        for fromQ, toQ in zip(fromQs, toQs):
            # append quantum teleport operation with total qubits, from, to, and auxiliary qubit
            teleport_qc.compose(quantum_teleport(circuit_span, fromQ, toQ, circuit_span-1), qubits=range(circuit_span), inplace=True)
            teleport_qc.reset(10)  # reset auxiliary qubit for next teleportation
        return teleport_qc

    # Portion of protocol that measures the sent message with another set of bases, translating back into classical info
    # Returns a quantum circuit with `key_len` quantum registers and `key_len` classical registers
    def measure_qubits(self, bases: list):
        measure_qc = QuantumCircuit(len(bases), len(bases))
        for qubit_pos, base in enumerate(bases):
            if base == 0:  # Z basis measurement
                measure_qc.measure(qubit_pos, qubit_pos)
            else:  # X basis measurement
                measure_qc.h(qubit_pos)
                measure_qc.measure(qubit_pos, qubit_pos)
        return measure_qc

    # Creates and runs a master circuit for the entire "sender" portion of the protocol; returns the resulting state
    def sender_protocol(self):
        self.reset()
        # Step 1: encode on sender's end
        self.masterQC.compose(
            self.encode_qubits(
                utils.get_random_numbers(self.key_len, self.sim),
                utils.get_random_numbers(self.key_len, self.sim)
            ),
            qubits=range(self.key_len), inplace=True
        )

        # Step 2: teleport to receiver
        self.masterQC.compose(
            self.bulk_teleport(
                list(range(self.key_len)),
                list(range(self.key_len, 2*self.key_len))
            ),
            qubits=range(2*self.key_len+1), inplace=True
        )
        self.masterQC.save_statevector()
        return self.sim.run(transpile(self.masterQC, self.sim)).result().get_statevector()

    # Creates and runs a master circuit for the entire "receiver" portion of the protocol; returns the measured key
    def receiver_protocol(self, state):
        # Restore the state from the sender portion (workaround to substitute for actual transmission of quantum info)
        self.masterQC = QuantumCircuit(2*self.key_len+1, self.key_len)
        self.masterQC.set_statevector(state)

        # Step 3: generate bases and measure message on receiver's end
        receiver_bases = utils.get_random_numbers(self.key_len, self.sim)
        self.receiver_bases = receiver_bases
        self.masterQC.compose(
            self.measure_qubits(receiver_bases),
            qubits=range(self.key_len, 2*self.key_len), clbits=range(self.key_len), inplace=True
        )
        qobj = assemble(self.masterQC, shots=1, memory=True)  # only run once and store results
        result = self.sim.run(qobj).result().get_memory()[0][::-1]

        # Step 4: prune invalid bits
        # (only keep the bits where both measured in the same basis; otherwise the results are not guaranteed to agree)
        key = ""
        for base_s, base_r, i in zip(self.sender_bases, self.receiver_bases, range(len(result))):
            if base_s == base_r:
                key += result[i]
        return key
