#!/bin/bash
echo "[BALORG-QUANTUM] Training Quantum TLM with persona-bound overlays..."
python3 quantum_tlm.py > ../circuits/joseph_awakens.qasm 2>&1
echo "[BALORG-QUANTUM] Training complete." >> ../logs/training.log
