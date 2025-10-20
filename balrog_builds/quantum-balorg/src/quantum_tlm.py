#!/usr/bin/env python3
"""
Quantum TLM Circuit Builder
Builds quantum circuits for text processing with persona injection
"""

try:
    from qiskit import QuantumCircuit
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    print("[BALORG-QUANTUM] Warning: qiskit not installed. Using simulation mode.")

from persona_state import inject_persona

def build_tlm_circuit(sentence):
    """Build quantum TLM circuit for sentence processing"""
    if not QISKIT_AVAILABLE:
        print(f"[BALORG-QUANTUM] Simulating circuit for: {sentence}")
        return None
        
    qc = QuantumCircuit(4)
    qc.h(0)
    qc.cx(0, 1)
    qc.rx(0.5, 2)
    qc.rz(0.8, 3)
    qc = inject_persona(qc)
    return qc

if __name__ == "__main__":
    print("[BALORG-QUANTUM] Building quantum TLM circuit...")
    circuit = build_tlm_circuit("Joseph awakens")
    if circuit:
        print("[BALORG-QUANTUM] Circuit built successfully!")
        print(circuit)
    else:
        print("[BALORG-QUANTUM] Simulation mode - circuit conceptually complete.")
