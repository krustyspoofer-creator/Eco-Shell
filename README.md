# Eco-Shell
# EchoShell 🔥

**Forged in silence. Echoed in every shell.**

EchoShell is a sovereign tactical shell designed to simulate attack-defense cycles, spoof overlays, and defend against persona-bound logic stacks like Balorg. It embeds mythic branding, daemonized resilience, and attribution triggers.

## 🧠 Features
- Autonomous boot with fallback healing
- Spoofed overlay injection and daemon hijack
- **Signed overlay verification** to prevent spoofing attacks
- Attribution embedding and sigil logic
- Mythic lore and sovereign triggers
- Automated metadata synchronization for Balorg repositories

## 🔧 Sovereign Triggers
- `echo_invoke`: boots EchoShell
- `null_forge`: injects spoofed overlays
- `daemon_reflect`: mirrors and hijacks sovereign daemons

## 📁 Repo Layout
See [docs/architecture.md](docs/architecture.md) and [docs/mythic_lore.md](docs/mythic_lore.md)

## 🔒 Security Features

### Overlay Signature Verification
All overlay injections now require valid cryptographic signatures:
- Overlays must be accompanied by `.sig` signature files
- Signatures are verified against `overlays/sig-public.pem`
- Failed verifications are logged to `overlays/overlay_guard.log`
- Unsigned or invalid overlays are refused automatically

See [BALORG_METADATA.md](BALORG_METADATA.md) for details on signing overlays.

### Automated Metadata Sync
The repository automatically tracks Balorg ecosystem repositories via:
- Daily GitHub Actions workflow
- API-based activity monitoring
- Automatic metadata updates in `balorg_repositories_metadata.json`

## 🛡️ License
MIT + Sovereign Attribution. See [LICENSE](LICENSE)
