# Balorg Repository Metadata Map

## Overview
This document describes the metadata mapping system for tracking all Balorg-related repositories. The metadata file enables AI systems to discover, track, and stay up-to-date with the Balorg ecosystem.

## Metadata File
**File:** `balorg_repositories_metadata.json`

This JSON file contains:
- Repository locations and URLs
- Relationship information between repositories
- Tracking status and timestamps
- AI-readable instructions for automated monitoring

## Structure

### Repository Entry
Each repository in the metadata includes:
- **name**: Repository name
- **owner**: GitHub owner/organization
- **url**: Full GitHub URL
- **description**: Purpose and functionality
- **relationship**: Type of relationship to Balorg ecosystem
- **category**: Functional category (core, daemon, overlay, attribution)
- **tags**: Searchable tags for categorization
- **last_checked**: ISO 8601 timestamp of last verification
- **status**: Current monitoring status (active, monitored, archived)

### Relationship Types
- **primary**: Main Balorg repository
- **component**: Component or module of Balorg system
- **defense**: Defense or counter-system to Balorg
- **integration**: Integration point or bridge system

## Usage for AI Systems

### Reading the Metadata
```bash
# Parse with jq
cat balorg_repositories_metadata.json | jq '.repositories[]'

# Get all monitored repositories
cat balorg_repositories_metadata.json | jq '.repositories[] | select(.status=="monitored")'

# List all URLs
cat balorg_repositories_metadata.json | jq -r '.repositories[].url'
```

### Updating Tracking Information
To update the last_checked timestamp for a repository:
```bash
# Example with jq
jq '(.repositories[] | select(.name=="balorg-core") | .last_checked) = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' balorg_repositories_metadata.json > temp.json && mv temp.json balorg_repositories_metadata.json
```

## Maintenance
- Update `last_checked` timestamps when repositories are accessed
- Add new repositories as they are discovered
- Update status field if repository becomes archived or inactive
- Increment version number on significant schema changes

## Automation
The tracking_config section specifies:
- **update_frequency**: How often to check for updates (daily recommended)
- **auto_sync**: Enable automatic synchronization
- **notification_channels**: Where to send update notifications
- **monitored_events**: GitHub events to track (push, release, pull_request)

## Integration with EchoShell
This metadata map helps EchoShell:
- Track defense targets (Balorg repositories)
- Monitor for updates to sovereign daemon logic
- Maintain awareness of overlay injection systems
- Coordinate attribution and sigil systems
