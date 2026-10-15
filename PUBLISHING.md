# Maintain and release the research repository

The project is hosted at [Small-ed1/accord-can-research](https://github.com/Small-ed1/accord-can-research) as a **private repository**. The initial history preserves the imported 0.1.0 draft, followed by repository-completion changes. Commits use a project display name and the owner's GitHub no-reply email. Hosting under an account can identify authorship despite file sanitization.

No reuse license has been applied. Read [LICENSING.md](LICENSING.md) before changing distribution terms. A public visibility change is a separate maintainer decision. Keep private source captures and media outside the repository.

## Validate changes

Run the dependency-free tests from the repository root:

```sh
python -W error::ResourceWarning -m unittest discover -s tests -v
```

Run the full suite, including strict third-party DBC import:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -W error::ResourceWarning -m unittest discover -s tests -v
```

On Windows, use `.venv\Scripts\python.exe`. The importer is a development dependency; the decoder and auditor remain standard-library-only. CI tests Python 3.10 and 3.14, both with and without cantools. An absent importer is an explicit skip in local standard-library runs, and is required in CI's qualification jobs.

## Refresh release integrity

Stage only reviewed publication files. Inspect `git diff --cached --stat` and the staged diff for accidental logs, readings, identifiers or credentials. Update the release notes, changelog, verification report and sanitized test transcript when their contents change.

Regenerate the manifest from staged file contents with this command. It works in a Git checkout and never traverses ignored private inputs or the virtual environment:

```sh
python - <<'PY'
from pathlib import Path
import hashlib
import subprocess

names = subprocess.check_output(['git', 'ls-files', '-z']).decode().split('\0')
rows = []
for name in sorted(filter(None, names)):
    if name == 'MANIFEST.sha256':
        continue
    content = subprocess.check_output(['git', 'show', f':{name}'])
    rows.append(f'{hashlib.sha256(content).hexdigest()}  {name}\n')
Path('MANIFEST.sha256').write_text(''.join(rows), encoding='utf-8', newline='\n')
PY
git add MANIFEST.sha256
sha256sum -c MANIFEST.sha256
```

Stage all intended changes before regenerating. The hash check reads working files, so a staged/working-tree discrepancy fails validation. CI checks both hashes and complete coverage of tracked files. `.gitattributes` keeps text line endings consistent across checkouts.

## Create a research release

After committing, pushing, and confirming the validation workflow passed for that commit:

```sh
gh release create v0.1.0 --repo Small-ed1/accord-can-research \
  --target main --prerelease --title '0.1.0 research publication' \
  --notes-file RELEASE_NOTES.md
```

This is the initial release command; future releases require a new version and corresponding notes. A prerelease marks the research's provisional scope. Releases in a private repository retain its access restrictions. GitHub provides source archives; do not attach private inputs, the original source collection or local environment files.

The [remaining-signal register](docs/unresolved.md) describes what needs new evidence. A repository release does not settle those measurements or qualify the software on a vehicle.
