#!/usr/bin/env python3
"""Check that a private copy is serving exactly the release it says it is.

    python3 tools/verify-release.py <copy address> [kept copy of the list]

The published lists: https://github.com/ezbrzys/corkly-releases (releases/<release>.json).

Fetches https://<copy>/release.json, then every site file it lists, and compares each file's
SHA-256 with the list. Given a copy of the release file kept somewhere the site can't change
(the repo, or one sent to the studio at release time), it first checks the live list matches it.
Exit code 0 only if everything matches. Standard library only, so a security team can run it as is.
"""
import hashlib, json, sys, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'corkly-verify-release', 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read()

if len(sys.argv) < 2: sys.exit(__doc__)
host = sys.argv[1].replace('https://', '').strip('/')
live = json.loads(get('https://%s/release.json' % host))
bad = 0
if len(sys.argv) > 2:
    kept = json.load(open(sys.argv[2]))
    if kept != live: print('✗ The live release list differs from', sys.argv[2]); bad += 1
    else: print('✓ The live release list matches', sys.argv[2])
print('Release %s at %s (commit %s)' % (live['release'], host, live.get('commit', '?')[:12]))
for path, want in sorted(live['site'].items()):
    url = 'https://%s%s' % (host, path)
    if path.endswith('.js') or path.endswith('.css'): url += '?v=' + live['release']   # as the app loads them
    try: got = hashlib.sha256(get(url)).hexdigest()
    except Exception as e: print('✗', path, '— could not fetch:', e); bad += 1; continue
    if got != want: print('✗', path, 'differs'); bad += 1
print(('✓ All %d files match.' % len(live['site'])) if not bad else ('✗ %d problem(s).' % bad))
sys.exit(1 if bad else 0)
