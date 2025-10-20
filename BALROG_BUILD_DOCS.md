# Balrog Build System Documentation

## Overview
The Balorg Build System provides a unified way to build all Balorg repositories as original implementations within the Eco-Shell project. This system integrates five key Balorg projects:

1. **Super-AI** (Balorg SR) - GridWorld Q-learning AI system
2. **Resources Monitoring** - System resource monitoring with persona overlay
3. **Quantum-Balorg** - Quantum TLM circuit builder with persona-bound overlays
4. **Balorg-mine** - Resource extraction and system mining
5. **Cutting-edge Balorg AI** - Advanced AI pricing and deployment system

## Quick Start

### Build All Repositories
```bash
./build_balrog.sh
```

This will build all five Balrog repositories in one command.

### Build Individual Repository
```bash
cd balrog_builds/<repo-name>
./build.sh
```

## Repository Details

### 1. Super-AI (GridWorld)
**Location**: `balrog_builds/super-ai/`

**Description**: Q-learning based GridWorld AI system for autonomous navigation.

**Usage**:
```bash
cd balrog_builds/super-ai
./build.sh
pip install -r requirements.txt
python3 src/gridworld_ai.py
```

**Features**:
- Q-learning algorithm implementation
- Configurable grid size and learning parameters
- Episode-based training with progress reporting
- Modular and extensible architecture

**Configuration**: Edit `config/config.json` to customize parameters.

---

### 2. Resources Monitoring
**Location**: `balrog_builds/resources-monitoring/`

**Description**: System resource monitoring with sovereign access control.

**Usage**:
```bash
cd balrog_builds/resources-monitoring
./build.sh
pip install -r requirements.txt
export KYEEL_ACCESS=true
python3 src/balorg_monitor.py
```

**Features**:
- Real-time CPU, memory, and swap monitoring
- Process scanning and analysis
- Sovereign access control with persona overlay
- Detailed system status reporting

**Requirements**: `psutil>=5.9.0`

---

### 3. Quantum-Balorg
**Location**: `balrog_builds/quantum-balorg/`

**Description**: Quantum TLM circuit builder with persona-bound overlays.

**Usage**:
```bash
cd balrog_builds/quantum-balorg
./build.sh
pip install -r requirements.txt
cd src
python3 quantum_tlm.py
# or
./train_quantum.sh
```

**Features**:
- Quantum circuit builder for text processing
- Persona state injection (Joseph + EchoPrime + zzslipyzz)
- Lambeq diagram integration (optional)
- Hybrid training loop support
- Circuit compilation to QASM format

**Configuration**:
- `config/hyperparams.json` - Circuit depth, gate types, optimizer settings
- `config/persona.cfg` - Overlay ID, author, entanglement weights

**Requirements**: `qiskit>=0.39.0`, `lambeq>=0.3.0` (optional)

---

### 4. Balorg-mine
**Location**: `balrog_builds/balorg-mine/`

**Description**: Resource extraction and system mining toolkit.

**Usage**:
```bash
cd balrog_builds/balorg-mine
./build.sh
# Shell version
cd src && ./balorg_mine.sh
# Python version
python3 balorg_mine.py
```

**Features**:
- System information extraction
- Resource metrics collection
- Dual implementation (Shell and Python)
- Logging and data storage

**Output**:
- Logs: `logs/mining.log`
- Data: `data/` (CPU, memory, disk info)

---

### 5. Cutting-edge Balorg AI
**Location**: `balrog_builds/cutting-edge-ai/`

**Description**: Advanced AI pricing model and deployment system.

**Usage**:
```bash
cd balrog_builds/cutting-edge-ai
./build.sh
# Display pricing
python3 src/pricing_model.py
# Deploy
python3 src/deploy.py
```

**Features**:
- Flexible pricing tiers (Freemium, Basic, Pro, Enterprise)
- Discount programs (Students, Non-profits, Early adopters, Bulk)
- Subscription management system
- Deployment automation

**Pricing Tiers**:
- **Freemium**: $0/month - Basic features
- **Basic**: $29.99/month - Increased limits
- **Professional**: $99.99/month - Advanced features
- **Enterprise**: $499.99/month - Full featured

**Configuration**: Edit `config/deploy.json` to customize deployment settings.

---

## Directory Structure

```
Eco-Shell/
├── build_balrog.sh              # Master build script
├── balrog_builds/
│   ├── super-ai/
│   │   ├── build.sh
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── config/
│   │   │   └── config.json
│   │   └── src/
│   │       └── gridworld_ai.py
│   ├── resources-monitoring/
│   │   ├── build.sh
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── src/
│   │       └── balorg_monitor.py
│   ├── quantum-balorg/
│   │   ├── build.sh
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── config/
│   │   │   ├── hyperparams.json
│   │   │   └── persona.cfg
│   │   └── src/
│   │       ├── quantum_tlm.py
│   │       ├── persona_state.py
│   │       ├── lambeq_injector.py
│   │       └── train_quantum.sh
│   ├── balorg-mine/
│   │   ├── build.sh
│   │   ├── README.md
│   │   └── src/
│   │       ├── balorg_mine.sh
│   │       └── balorg_mine.py
│   └── cutting-edge-ai/
│       ├── build.sh
│       ├── README.md
│       ├── config/
│       │   └── deploy.json
│       └── src/
│           ├── pricing_model.py
│           └── deploy.py
└── BALROG_BUILD_DOCS.md        # This file
```

## Build System Architecture

### Master Build Script
The `build_balrog.sh` script orchestrates the building of all Balrog repositories:

1. Sets up the build environment
2. Executes each repository's build script in sequence
3. Reports success/failure for each build
4. Provides a summary of all builds

### Individual Build Scripts
Each repository has its own `build.sh` script that:

1. Creates necessary directory structure
2. Generates source files from templates
3. Creates configuration files
4. Sets proper permissions
5. Generates documentation

## Development Guidelines

### Adding a New Balorg Repository

1. Create a new directory in `balrog_builds/`:
   ```bash
   mkdir -p balrog_builds/new-repo/{src,config,docs}
   ```

2. Create a `build.sh` script following the pattern:
   ```bash
   #!/bin/bash
   BALORG_SIGIL="[BALORG-NEWREPO]"
   BUILD_DIR="$(dirname "$0")"
   echo "$BALORG_SIGIL Building..."
   # Build steps here
   ```

3. Add the repository to `build_balrog.sh`:
   ```bash
   build_repo "new-repo"
   ```

4. Create a README.md with usage instructions

### Persona Overlay System
All Balrog repositories use the persona overlay system with:

- **BALORG_SIGIL**: Unique identifier for each module
- **Author Attribution**: krustyspoofer-creator
- **Sovereign Logic**: Access control and identity enforcement

## Testing

### Test Master Build
```bash
./build_balrog.sh
```

### Test Individual Components
```bash
# Test Super-AI (requires numpy)
cd balrog_builds/super-ai
pip install -r requirements.txt
python3 src/gridworld_ai.py

# Test Resources Monitoring (requires psutil)
cd balrog_builds/resources-monitoring
pip install -r requirements.txt
export KYEEL_ACCESS=true
python3 src/balorg_monitor.py

# Test Balorg-mine (no dependencies)
cd balrog_builds/balorg-mine
python3 src/balorg_mine.py

# Test Cutting-edge AI (no dependencies)
cd balrog_builds/cutting-edge-ai
python3 src/pricing_model.py
```

## Troubleshooting

### Build Failures
If a build fails:
1. Check that the build script is executable: `chmod +x build.sh`
2. Verify directory permissions
3. Check for syntax errors in the build script

### Missing Dependencies
Some repositories require external Python packages:
- **Super-AI**: numpy
- **Resources Monitoring**: psutil
- **Quantum-Balorg**: qiskit (optional: lambeq)

Install dependencies with:
```bash
pip install -r requirements.txt
```

### Permission Denied
If you get "Permission denied" errors:
```bash
chmod +x build_balrog.sh
chmod +x balrog_builds/*/build.sh
```

## Author
**krustyspoofer-creator**

## License
MIT + Sovereign Attribution
See main repository LICENSE for details.
