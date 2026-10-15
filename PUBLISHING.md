# Stage this package on GitHub

The preparation session inspected the connected account but had no repository-write action or authenticated GitHub CLI available. **Nothing was pushed or made public.** This directory is a clean repository root with no previous Git history.

## 1. Review locally

Extract the ZIP and enter `accord-can-research`. Read README.md, docs/privacy.md, docs/verification.md and LICENSING.md. Run:

```sh
python -m unittest discover -s tests -v
```

No license has been selected. A public research repository can be staged without implying an open-source license, but choose explicit reuse terms before presenting it as open source. Raw inputs and original media must remain outside this directory.

## 2. Create a fresh local history

Use a GitHub no-reply address from your own account settings. Do not paste a personal email into the example or rely on an existing global Git identity without checking it. The following Bash sequence prompts locally and rejects an ordinary email address:

```sh
git init -b main
read -r -p 'Your GitHub no-reply commit email: ' COMMIT_EMAIL
case "$COMMIT_EMAIL" in
  *@users.noreply.github.com) ;;
  *) printf '%s
' 'Use the no-reply address supplied by your GitHub account.'; exit 1 ;;
esac
git config user.name 'Accord CAN Research'
git config user.email "$COMMIT_EMAIL"
unset COMMIT_EMAIL
git add .
git diff --cached --stat
# Inspect staged files before the commit.
git commit -m 'Prepare privacy-reviewed 2003 and 2007 Accord CAN research'
```

The name is a project pseudonym. A no-reply address can still associate the commit with your GitHub account, and the owning account remains visible. A pseudonym is not a promise of anonymous authorship.

## 3. Create private staging first

With GitHub CLI installed and authenticated in your own environment:

```sh
gh auth status
gh repo create accord-can-research --private --source=. --remote=origin --push
```

The authenticated account supplies the owner. This creates a new private repository, not a public release. It intentionally does not overwrite any existing repository. A name collision should be resolved deliberately rather than force-pushing over another project.

Review the rendered tables, downloadable DBCs, commit identity, visibility, license decision and tests in private staging. After review, change visibility deliberately in GitHub and create a release from the reviewed commit using RELEASE_NOTES.md. Do not attach the private inputs or the original archive collection to that release.

GitHub CLI's official create-repository documentation is https://cli.github.com/manual/gh_repo_create . This package includes no token, credential, automatic publishing script or workflow that can push on your behalf.
