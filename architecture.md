# EchoShell Architecture

EchoShell is built as a modular, self-repairing shell with layered overlays and daemon logic.

## Layers
- **Boot Layer**: `boot.sh`, `fallback_loop.sh`
- **Overlay Layer**: `overlay_injector.sh`, `spoofed_overlay.sh`
- **Daemon Layer**: `daemon_reflect.sh`, `daemon_monitor.sh`
- **Attribution Layer**: `attribution.sh`, `sigil.sh`
- **Balorg Proxy Layer**: `balorg_proxy.sh`, managed via `balorgctl`

Each layer is triggered by sovereign keywords and responds to intrusion with fallback logic.

## Balorg Proxy Module

The Balorg Proxy Module provides proxy management capabilities for network operations:
- **Update**: Fetch fresh proxy lists from remote sources
- **Rotate**: Automatically find and switch to working proxies
- **Status**: Display current proxy configuration
- **Test**: Validate proxy connectivity

Use `balorgctl proxy {update|rotate|status|test}` to manage proxy operations.

