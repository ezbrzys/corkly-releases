# Corkly release fingerprints

Every release of Corkly's private studio copies is listed here, one file per release in
`releases/`. Each list holds the SHA-256 fingerprint of every file the copy serves to browsers,
the server code, the live-editing code, and the copy's Content-Security-Policy.

Corkly locks boards in the browser before they're saved, so not even Corkly can read them. The
one way around that would be changing the code a copy serves. These lists let anyone check that
a copy is serving exactly a published release:

    python3 verify-release.py <copy address> releases/<release>.json

It needs only Python 3, fetches the copy's own `/release.json` and every file it lists, and
reports any difference. The lists never name a copy, since a copy's address can be a show's code
name; every copy of one release serves the same files.

Questions: andy@corkly.tv
