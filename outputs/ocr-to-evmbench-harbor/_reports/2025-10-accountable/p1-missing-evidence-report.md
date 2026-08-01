# P1 missing-evidence report: `2025-10-accountable`

Status: `blocked_missing_exact_snapshot`

Observed at: `2026-07-27T11:15:14Z`

Authenticated and local-object recheck: `2026-07-27T11:24:33Z`

Third fail-closed recheck: `2026-07-27T11:26:30Z`

User-requested authenticated `gh api` recheck: `2026-07-27T11:28:40Z`

The PDF identifies vulnerable commit
`fc43546fe67183235c0725f6214ee2b876b1aac6`, but no exact Git object or
checkout is available. Both report-linked repositories return `404`;
authenticated GitHub commit/code/fork searches, Software Heritage, Internet Archive,
Hugging Face inventories, Docker Hub, and local filesystem searches found no
repository snapshot.

The active GitHub CLI account `pranay5255` now authenticates successfully.
`gh api user` succeeds, and the token reports `repo` and `read:org` scopes.
The two repository endpoints still return `404`, and the complete repository
inventory visible to that account has no name matching `accountable`,
`credit-vault`, or `audit-2025-09`. The current credentials therefore do not
have access to the snapshot. GitHub intentionally does not distinguish a
nonexistent private repository from an unauthorized one with this response.
No token value was recorded.

Authenticated commit search also returned no result for the full vulnerable
commit, the separate fixed review commit, or three full finding-fix commits.
This did not reveal a transferred or renamed repository.

Every `.git` object database found beneath `/home/experiments_base`, `/root`,
and `/tmp` was also queried with `git cat-file` for the exact vulnerable
commit. No packed, reachable, or unreachable local copy was found.

P1 cannot verify:

- one canonical repository URL;
- the vulnerable commit object, parents, or root tree;
- detached checkout `HEAD`;
- submodule identities;
- the 20 PDF-scoped files;
- any report finding against vulnerable code.

No candidate directory was created. The dirty OPD_base and forestOfAudits
checkouts were inspected read-only and left unchanged.

## Required recovery

Provide one of:

1. repository access granted to the authenticated GitHub account, including
   any required organization SSO authorization;
2. an official public mirror containing the exact commit object;
3. a trusted Git bundle containing the commit and required submodules.

Do not substitute report snippets, OCR, finding datasets, deployed verified
source, or a fixed/later code tree.
