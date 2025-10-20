# Quantum-Balorg
Quantum TLM Circuit Builder with persona-bound overlays

## Features
- Quantum circuit builder for text processing
- Persona state injection (Joseph + EchoPrime + zzslipyzz)
- Lambeq diagram integration (optional)
- Hybrid training loop

## Structure
```
quantum-balorg/
├── src/
│   ├── quantum_tlm.py            # Quantum circuit builder
│   ├── lambeq_injector.py        # Sentence to quantum diagram mapper
│   ├── persona_state.py          # Mythic identity injection
│   └── train_quantum.sh          # Training script
├── circuits/
│   └── joseph_awakens.qasm       # Sample compiled circuit
├── logs/
│   └── training.log
└── config/
    ├── hyperparams.json          # Circuit configuration
    └── persona.cfg               # Overlay identity
```

## Build
```bash
./build.sh
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Run
```bash
cd src
python3 quantum_tlm.py
# or
./train_quantum.sh
```

## Author
krustyspoofer-creator
