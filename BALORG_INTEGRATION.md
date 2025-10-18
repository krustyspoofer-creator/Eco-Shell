# Balorg AI Framework - Integration Guide

## Overview

The Balorg AI framework has been successfully integrated into Eco-Shell as a pure Bash-native AI system. This document provides guidance on using Balorg with EcoShell.

## Architecture

```
Eco-Shell/
├── Boot.Sh                      # EcoShell boot script
├── Fallback_loop.sh             # EcoShell fallback system
├── Overlay_injector.sh          # EcoShell overlay injection
├── Demon monitor                # EcoShell daemon monitor
├── Demon reflect                # EcoShell daemon reflection
└── balorg/                      # Balorg AI Framework
    ├── balorgctl                # Main control script
    ├── README.md                # Detailed documentation
    ├── QUICKSTART.sh            # Quick start guide
    ├── core/                    # Core functionality
    │   ├── plugin_runner.sh     # Plugin execution engine
    │   └── injection_manager.sh # Dynamic injection system
    ├── plugins/                 # Plugin collection
    │   ├── example_plugin.sh
    │   ├── system_info.sh
    │   ├── echo_analyzer.sh
    │   └── log_aggregator.sh
    ├── utils/                   # Utility functions
    │   ├── env_helper.sh
    │   └── json_helper.sh
    ├── api/                     # API emulation
    │   └── rest_emulator.sh
    ├── tests/                   # Test suite
    │   ├── test_balorgctl.sh
    │   ├── test_plugins.sh
    │   └── test_plugin_runner.sh
    └── examples/                # Example scripts
        └── integration_example.sh
```

## Quick Start

### 1. Initialize Balorg

```bash
cd balorg
./balorgctl init
```

### 2. Check Status

```bash
./balorgctl status
```

### 3. List Available Plugins

```bash
./balorgctl plugin list
```

### 4. Run the Quick Start Guide

```bash
./QUICKSTART.sh
```

### 5. Try the Integration Example

```bash
./examples/integration_example.sh
```

## Key Features

### 1. Pure Bash Implementation
- No Python, no external frameworks
- POSIX-compliant where possible
- Minimal dependencies (bash, jq, curl, socat)

### 2. Plugin System
- Modular plugin architecture
- TCP-based plugin service (port 50051)
- Easy plugin development

### 3. Injection Framework
- Dynamic code injection
- Create, execute, list, and remove injections
- Full logging support

### 4. API Emulation
- REST API emulator using netcat/curl
- gRPC-style endpoints with socat
- JSON support via jq

### 5. EcoShell Integration
- Seamless integration with existing EcoShell components
- EcoShell analyzer plugin
- Combined Balorg-EcoShell injections

## Usage Examples

### Example 1: Run a Plugin

```bash
cd balorg
./balorgctl plugin list
bash plugins/system_info.sh "test"
```

### Example 2: Create and Execute an Injection

```bash
cd balorg
./balorgctl injection create my_task 'echo "Task executed at $(date)"'
./balorgctl injection execute my_task
./balorgctl injection remove my_task
```

### Example 3: Analyze EcoShell Components

```bash
cd balorg
bash plugins/echo_analyzer.sh "analysis"
```

### Example 4: Start Plugin Service

```bash
cd balorg
# Start service in background
./balorgctl serve &
SERVICE_PID=$!

# In another terminal (if socat is available)
echo "example_plugin test_data" | socat - TCP:localhost:50051

# Stop service
kill $SERVICE_PID
```

### Example 5: Integrate with EcoShell

```bash
# From Eco-Shell root directory

# Initialize Balorg
./balorg/balorgctl init

# Create EcoShell integration
./balorg/balorgctl injection create eco_boot '
export OVERLAY_ID="BalorgEcho"
export BALORG_MODE="bash"
bash Boot.Sh
'

# Execute
./balorg/balorgctl injection execute eco_boot
```

## Command Reference

### balorgctl Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize Balorg environment |
| `status` | Show system status |
| `plugin list` | List available plugins |
| `plugin run <name> <data>` | Run a plugin |
| `serve` | Start plugin TCP service |
| `api` | Start REST API emulator |
| `injection create <name> <code>` | Create injection |
| `injection execute <name>` | Execute injection |
| `injection list` | List injections |
| `injection remove <name>` | Remove injection |
| `logs [plugin]` | View logs |
| `help` | Show help |

## Testing

### Run All Tests

```bash
cd balorg

# Test balorgctl and framework
bash tests/test_balorgctl.sh

# Test individual plugins
bash tests/test_plugins.sh
```

### Manual Testing

```bash
cd balorg

# Test a specific plugin
bash plugins/example_plugin.sh "test_data"

# Test injection system
./balorgctl injection create test 'echo "Test successful"'
./balorgctl injection execute test
./balorgctl injection remove test
```

## Configuration

Set environment variables before running Balorg:

```bash
export BALORG_HOME="/path/to/balorg"
export BALORG_MODE="bash"
export BALORG_API_PORT="8080"
```

## Dependencies

### Required
- `bash` (>= 4.0)

### Optional (for full functionality)
- `socat` - TCP plugin service
- `jq` - JSON processing
- `curl` - HTTP requests
- `nc` (netcat) - REST API emulator

### Check Dependencies

```bash
cd balorg
./balorgctl status
```

## Integration Patterns

### Pattern 1: EcoShell Boot with Balorg

```bash
#!/bin/bash
# Enhanced boot script with Balorg

# Initialize Balorg
source balorg/balorgctl
balorgctl init

# Original EcoShell boot
export OVERLAY_ID="EchoShell"
export TRIGGER_KEY="echo_invoke"

# Create Balorg logging injection
balorgctl injection create boot_log 'echo "Boot started at $(date)" >> balorg/logs/boot.log'
balorgctl injection execute boot_log

# Continue with EcoShell boot
bash ./Fallback_loop.sh
```

### Pattern 2: Daemon Monitoring with Balorg

```bash
# Create a daemon monitor injection
./balorg/balorgctl injection create daemon_watch '
if pgrep -f "daemon_reflect" > /dev/null; then
    echo "[Balorg] daemon_reflect is running"
else
    echo "[Balorg] daemon_reflect is not running - attempting recovery"
    bash ./Fallback_loop.sh
fi
'

# Run periodically
while true; do
    ./balorg/balorgctl injection execute daemon_watch
    sleep 60
done
```

### Pattern 3: Plugin-Based Analysis

```bash
# Use Balorg plugins to analyze EcoShell
bash balorg/plugins/echo_analyzer.sh "full"
bash balorg/plugins/system_info.sh "system"
bash balorg/plugins/log_aggregator.sh "logs"
```

## Security Notes

- Review all injections before execution
- Secure the `balorg/logs/` directory
- Use encryption for sensitive communications
- Limit access to `balorg/injections/` directory
- TCP services listen on localhost by default

## Troubleshooting

### Issue: Missing dependencies

**Solution:** Install required packages:
```bash
# Ubuntu/Debian
sudo apt-get install socat jq curl netcat

# macOS
brew install socat jq curl netcat
```

### Issue: Plugin not found

**Solution:** Check plugin exists and is executable:
```bash
ls -la balorg/plugins/
chmod +x balorg/plugins/*.sh
```

### Issue: Injection fails to execute

**Solution:** Check injection syntax:
```bash
./balorg/balorgctl injection list
cat balorg/injections/<injection_name>.sh
```

### Issue: Permission denied

**Solution:** Make scripts executable:
```bash
chmod +x balorg/balorgctl
chmod +x balorg/core/*.sh
chmod +x balorg/plugins/*.sh
```

## Development

### Creating New Plugins

```bash
cat > balorg/plugins/my_plugin.sh << 'EOF'
#!/usr/bin/env bash
# My custom plugin

data="$1"
echo "[my_plugin] Processing: $data"

# Your logic here

echo "[my_plugin] Done"
EOF

chmod +x balorg/plugins/my_plugin.sh
```

### Creating New Utilities

```bash
cat > balorg/utils/my_util.sh << 'EOF'
#!/usr/bin/env bash
# My utility functions

my_function() {
    local param="$1"
    echo "Processing: $param"
}

export -f my_function
EOF
```

## Next Steps

1. **🧩 Build Balorg Injection Framework** - Already implemented! ✓
2. **⚙️ Create Balorg gRPC-emulated API layer** - REST API emulator included ✓
3. **🕸️ Build Echo Knowledge Graph ingestion system** - Ready for implementation

To build the Knowledge Graph system:
```bash
# Create knowledge graph plugin
cat > balorg/plugins/knowledge_graph.sh << 'EOF'
#!/usr/bin/env bash
# Knowledge graph ingestion plugin
# TODO: Implement graph operations
EOF
```

## License

MIT + Sovereign Attribution (see LICENSE in repository root)

## Support

For detailed documentation, see `balorg/README.md`

For issues or questions, open an issue in the repository.

---

**Balorg AI - Bash-Native Framework**  
*Forged in pure shell. Echoed through modules.*
