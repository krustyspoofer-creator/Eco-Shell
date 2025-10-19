#!/usr/bin/env python3
"""Check Balorg repositories via the GitHub API and update last_checked timestamps."""
import os
import json
import sys
from datetime import datetime, timezone

try:
    import requests
except Exception:
    print("requests module not found, please install via pip")
    sys.exit(1)

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
META_PATH = 'balorg_repositories_metadata.json'

def now_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def get_latest_activity(owner, repo):
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    urls = [
        f'https://api.github.com/repos/{owner}/{repo}/commits',
        f'https://api.github.com/repos/{owner}/{repo}/releases',
        f'https://api.github.com/repos/{owner}/{repo}/events'
    ]
    latest = None
    for url in urls:
        try:
            r = requests.get(url, headers=headers, params={'per_page': 1}, timeout=10)
            if r.status_code != 200:
                continue
            data = r.json()
            if not data:
                continue
            item = data[0]
            # different endpoints have different timestamp fields
            for key in ('commit', 'published_at', 'created_at', 'updated_at'):
                if isinstance(item, dict) and key in item:
                    ts = item.get(key)
                    if ts:
                        latest = ts if (not latest or ts > latest) else latest
            # commits endpoint: item['commit']['committer']['date']
            if 'commit' in item:
                c = item['commit']
                if 'committer' in c and isinstance(c['committer'], dict):
                    ts = c['committer'].get('date')
                    if ts:
                        latest = ts if (not latest or ts > latest) else latest
        except Exception:
            continue
    return latest


def main():
    changed = False
    try:
        with open(META_PATH, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except Exception as e:
        print(f'Failed to read {META_PATH}: {e}')
        sys.exit(1)

    repos = meta.get('repositories', [])
    for r in repos:
        owner = r.get('owner')
        name = r.get('name')
        if not owner or not name:
            continue
        latest = None
        try:
            latest = get_latest_activity(owner, name)
        except Exception:
            latest = None

        now = now_iso()
        if r.get('last_checked') != now or (latest and r.get('last_activity') != latest):
            r['last_checked'] = now
            if latest:
                r['last_activity'] = latest
            changed = True
            print(f'Updated {owner}/{name}: last_checked={now}, last_activity={latest}')

    if changed:
        with open(META_PATH, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
    else:
        print('No updates necessary')

if __name__ == '__main__':
    main()
