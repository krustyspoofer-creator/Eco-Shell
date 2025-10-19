# Balorg Repositories Metadata

This file documents the automated metadata tracking system for Balorg-related repositories.

## Overview

The `balorg_repositories_metadata.json` file tracks repositories that are part of the Balorg ecosystem. This metadata is automatically synchronized daily via GitHub Actions.

## Metadata Structure

Each repository entry in the JSON file contains:
- `owner`: GitHub repository owner/organization
- `name`: Repository name
- `description`: Brief description of the repository
- `last_checked`: ISO 8601 timestamp of when the metadata was last verified
- `last_activity`: ISO 8601 timestamp of the most recent activity (commit, release, or event)

## Automated Synchronization

A GitHub Actions workflow (`.github/workflows/sync_balorg_metadata.yml`) runs daily at 02:00 UTC to:
1. Query the GitHub API for each repository
2. Update the `last_checked` timestamp to the current time
3. Update the `last_activity` timestamp with the latest commit/release/event time
4. Commit and push any changes back to the repository

The workflow also triggers on any manual push to `balorg_repositories_metadata.json`.

## Manual Updates

To manually run the metadata sync:

```bash
export GITHUB_TOKEN=your_token_here
python3 scripts/check_balorg_metadata.py
```

The script will update `balorg_repositories_metadata.json` with the latest information.

## Overlay Security Guard

To prevent overlay spoofing attacks, this repository implements signature verification for all overlay injections:

### How it Works

1. Each overlay must be accompanied by a `.sig` signature file
2. The signature is verified against the public key at `overlays/sig-public.pem`
3. If verification fails, the overlay injection is refused and logged
4. All injection attempts are logged to `overlays/overlay_guard.log`

### Usage

The overlay guard is automatically invoked by `Overlay_injector.sh` before any injection occurs. No manual intervention is required.

### Signing Overlays

To sign an overlay file:

```bash
# Generate signature (requires private key)
openssl dgst -sha256 -sign private-key.pem -out overlay.sig overlay_file

# Verify signature
openssl dgst -sha256 -verify overlays/sig-public.pem -signature overlay.sig overlay_file
```

## Security

- All overlay injections require valid signatures
- Failed verification attempts are logged
- The public key is stored in the repository for transparency
- Private keys are never committed to the repository
