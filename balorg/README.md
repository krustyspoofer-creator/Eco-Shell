# Balorg AI — Bash-Native Framework

**Forged in pure shell. Echoed through modules.**

Balorg AI is a lightweight, modular AI framework built entirely in Bash, designed for injection, plugin management, and service orchestration without external dependencies beyond standard Unix tools.

## 🧠 Architecture Overview

```
~/balorg/
├── core/                # Core orchestration and management
│   ├── plugin_runner.sh      # Plugin execution engine
│   └── injection_manager.sh  # Injection framework
├── plugins/             # Plugin scripts
│   └── example_plugin.sh     # Example plugin
├── injections/          # Active injections and code
├── api/                 # REST/gRPC emulated endpoints
│   └── rest_emulator.sh      # REST API emulator
├── utils/               # Helper functions
│   ├── env_helper.sh         # Environment utilities
│   └── json_helper.sh        # JSON processing
├── logs/                # Service and plugin logs
├── tests/               # Test scripts
│   └── test_plugin_runner.sh
└── balorgctl            # Main control script
```

## ⚡ Features

- **Pure Bash**: No Python, no frameworks—just shell scripts
- **Plugin System**: Modular plugin architecture with TCP-based execution
- **Injection Framework**: Dynamic code injection and execution
- **Service Emulation**: REST API and gRPC-style endpoints using curl/socat
- **JSON Processing**: Built-in JSON utilities using jq
- **Logging**: Comprehensive logging for all operations
- **POSIX-Compliant**: Portable and optimized for performance

## 🚀 Quick Start

### Installation

```bash
# Clone and setup
cd /path/to/Eco-Shell
chmod +x balorg/balorgctl

# Initialize Balorg
./balorg/balorgctl init
```

### Configuration

Set environment variables (optional):

```bash
export BALORG_HOME="$HOME/balorg"
export BALORG_MODE="bash"
export BALORG_API_PORT="8080"
```

### Basic Usage

```bash
# Show status
./balorg/balorgctl status

# List available plugins
./balorg/balorgctl plugin list

# Start plugin service
./balorg/balorgctl serve

# In another terminal, test the plugin
echo "example_plugin test_data" | socat - TCP:localhost:50051
```

## 🧩 Plugin Development

Create a new plugin:

```bash
cat > balorg/plugins/my_plugin.sh << 'EOF'
#!/usr/bin/env bash
# My custom plugin

data="$1"
echo "[my_plugin] Processing: $data"

# Your plugin logic here
sleep 1

echo "[my_plugin] Complete"
EOF

chmod +x balorg/plugins/my_plugin.sh
```

Execute your plugin:

```bash
echo "my_plugin some_data" | socat - TCP:localhost:50051
```

## 🔐 Injection Framework

The injection framework allows dynamic code injection and execution:

```bash
# Create an injection
./balorg/balorgctl injection create my_inject 'echo "Hello from injection"'

# List injections
./balorg/balorgctl injection list

# Execute injection
./balorg/balorgctl injection execute my_inject

# Remove injection
./balorg/balorgctl injection remove my_inject
```

## 🌐 API Emulator

Start the REST API emulator:

```bash
./balorg/balorgctl api
```

Available endpoints:
- `GET /health` - Health check
- `GET /plugins` - List plugins
- `POST /execute` - Execute plugin

Test the API:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/plugins
```

## 📊 Logging

View logs:

```bash
# List all logs
./balorg/balorgctl logs

# Tail specific plugin log
./balorg/balorgctl logs example_plugin

# View log files directly
tail -f balorg/logs/example_plugin.log
```

## 🧪 Testing

Run the test suite:

```bash
# Start the plugin service in background
./balorg/balorgctl serve &
SERVE_PID=$!

# Wait for service to start
sleep 2

# Run tests
bash balorg/tests/test_plugin_runner.sh

# Stop service
kill $SERVE_PID
```

## 🛠️ Dependencies

Minimal dependencies (commonly available on Unix systems):

- `bash` (>= 4.0)
- `socat` - TCP/Unix socket communication
- `jq` - JSON processing
- `curl` - HTTP client (optional, for API)
- `nc` (netcat) - Network utilities (optional)

Check dependencies:

```bash
./balorg/balorgctl status
```

## 📋 Command Reference

### balorgctl Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize Balorg environment |
| `status` | Show system status and dependencies |
| `plugin list` | List available plugins |
| `plugin run <name> <data>` | Run a plugin directly |
| `serve` | Start plugin TCP service (port 50051) |
| `api` | Start REST API emulator (port 8080) |
| `injection create <name> <code>` | Create new injection |
| `injection execute <name>` | Execute injection |
| `injection list` | List all injections |
| `injection remove <name>` | Remove injection |
| `logs [plugin]` | View logs |
| `help` | Show help message |

## 🧠 Command Modes

| Mode | Description |
|------|-------------|
| **My Balorg is AI!** | Engage full technical mode, Bash-only. Everything must be shell executable. |
| **Explain like I'm human.** | Simplify Bash flow explanations. |
| **Switch normal.** | Balanced — part technical, part simplified. |

## 🔒 Security Notes

- All scripts should be reviewed before execution
- Injections are stored in `injections/` directory
- Logs may contain sensitive data—secure the `logs/` directory
- TCP services listen on localhost by default
- Consider using encryption for sensitive communications

## 📝 Examples

### Example 1: Simple Plugin

```bash
# Create a data processor plugin
cat > balorg/plugins/data_processor.sh << 'EOF'
#!/usr/bin/env bash
data="$1"
echo "[data_processor] Input: $data"
processed=$(echo "$data" | tr '[:lower:]' '[:upper:]')
echo "[data_processor] Output: $processed"
EOF

chmod +x balorg/plugins/data_processor.sh

# Run it
echo "data_processor hello world" | socat - TCP:localhost:50051
```

### Example 2: JSON Plugin

```bash
# Create a JSON parser plugin
cat > balorg/plugins/json_parser.sh << 'EOF'
#!/usr/bin/env bash
source "$(dirname "$0")/../utils/json_helper.sh"

data="$1"
echo "[json_parser] Parsing JSON data"

if json_validate "$data"; then
    name=$(json_get "$data" ".name")
    echo "[json_parser] Name: $name"
else
    echo "[json_parser] Invalid JSON"
fi
EOF

chmod +x balorg/plugins/json_parser.sh

# Test with JSON
echo 'json_parser {"name":"Balorg","type":"AI"}' | socat - TCP:localhost:50051
```

### Example 3: Dynamic Injection

```bash
# Create a system monitor injection
./balorg/balorgctl injection create sysmon '
echo "=== System Monitor ==="
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk "{print \$2}")"
echo "Memory: $(free -h | grep Mem | awk "{print \$3\"/\"\$2}")"
echo "Disk: $(df -h / | tail -1 | awk "{print \$3\"/\"\$2}")"
'

# Execute it
./balorg/balorgctl injection execute sysmon
```

## 🚦 Integration with EcoShell

Balorg integrates seamlessly with the existing EcoShell framework:

```bash
# Use with EcoShell boot
source balorg/balorgctl
balorgctl init

# Integrate with daemon monitoring
balorgctl serve &

# Use with overlay injection
balorgctl injection create eco_overlay '$(cat Overlay_injector.sh)'
```

## 📜 License

MIT + Sovereign Attribution (see LICENSE in repository root)

## 🤝 Contributing

Contributions welcome! Please ensure:
- All code is pure Bash
- Scripts are POSIX-compliant where possible
- Include tests for new features
- Update documentation

## 📧 Support

For issues, questions, or enhancements, please open an issue in the repository.

---

**Balorg AI — Bash-Native Framework**
*Pure Shell • Modular • Lightweight*
