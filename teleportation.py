from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer, IBMQ
from qiskit.extensions import Initialize
from qiskit.quantum_info import random_statevector

# ####################################################################
#
# Source: https://qiskit.org/textbook/ch-algorithms/teleportation.html
#
# ####################################################################


def create_bell_pair(qc, a, b):
    """Creates a bell pair in qc using qubits a & b"""
    qc.h(a) # Put qubit a into state |+>
    qc.cx(a,b) # CNOT with a as control and b as target


def alice_gates(qc, psi, a):
    qc.cx(psi, a)
    qc.h(psi)


def measure_and_send(qc, a, b):
    """Measures qubits a & b and 'sends' the results to Bob"""
    qc.barrier()
    qc.measure(a,0)
    qc.measure(b,1)


def bob_gates(qc, qubit, crz, crx):
    # Here we use c_if to control our gates with a classical
    # bit instead of a qubit
    qc.x(qubit).c_if(crx, 1) # Apply gates if the registers
    qc.z(qubit).c_if(crz, 1) # are in the state '1'


def teleportation_protocol(qc, crz, crx):
    # STEP 1
    # Now begins the teleportation protocol
    create_bell_pair(qc, 1, 2)
    qc.barrier()

    #STEP 2
    # Send q1 to Alice and q2 to Bob
    alice_gates(qc, 0, 1)

    # STEP 3
    # Alice then sends her classical bits to Bob
    measure_and_send(qc, 0, 1)

    # STEP 4
    # Bob decodes qubits
    bob_gates(qc, 2, crz, crx)

    return qc


if __name__ == "__main__":
    psi = random_statevector(2)

    qr = QuantumRegister(3, name="q")   # Protocol uses 3 qubits
    crz = ClassicalRegister(1, name="crz") # and 2 classical registers
    crx = ClassicalRegister(1, name="crx")
    qc = QuantumCircuit(qr, crz, crx)
    qc.initialize(psi.data, [0])
    teleportation_circuit = teleportation_protocol(qc, crz, crx)
    teleportation_circuit.draw()

