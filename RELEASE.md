# Release Procedure

This document is the single source of truth for releasing the Smartsheet Python SDK. Publishing to PyPI is automated via GitHub Actions, but the changelog update is done by hand.

## Overview

Releases follow [Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/) conventions. Every release consists of:

1. A "Prepare for release" PR that closes out the changelog.
2. A merged commit on `mainline` published as a GitHub Release (which also creates the tag).
3. Automated publishing to PyPI triggered by the GitHub Release event.

> **Note:** There is no version file to bump. The version is derived entirely from the git tag at build time via `hatch-vcs`.

## Prerequisites

- Write access to the `smartsheet/smartsheet-python-sdk` repository.
- PyPI credentials are not needed locally — publishing uses a `PYPI_API_TOKEN` stored as a GitHub Actions secret.

## Step-by-Step Process

### 1. Decide the version bump

Review the `## [x.x.x] - Unreleased` section in `CHANGELOG.md` and apply semver rules:

| Change type | Bump |
| --- | --- |
| New endpoints, non-breaking additions | `minor` |
| Bug fixes, dependency updates | `patch` |
| Breaking API changes, removed types/methods | `major` |

### 2. Create a "Prepare for release" pull request

Open a branch from `mainline` (e.g., `release/v4.2.0`) and make the following change:

#### Update `CHANGELOG.md`

Feature PRs accumulate entries under `## [x.x.x] - Unreleased`. For the release, insert the new versioned header between that placeholder and its content:

```diff
 ## [x.x.x] - Unreleased

+## [4.2.0] - 2026-07-15
+
 ### Added
```

The `## [x.x.x] - Unreleased` placeholder header is never removed — it stays at the top of the file permanently so future PRs have somewhere to add entries.

#### PR title convention

```
Prepare for release vX.X.X
```

Example: `Prepare for release v4.2.0`

### 3. Merge the PR

CI must pass before merging. The `test-build.yaml` workflow runs:

- Markdown lint and pylint
- Tests across Python 3.10, 3.11, 3.12, 3.13, and 3.14
- Mock API SDK tests via WireMock
- Build package test
- Documentation build test

### 4. Create and publish the GitHub Release

1. Go to **Releases → Draft a new release** in the GitHub UI.
2. In the **Choose a tag** field, type the new version (e.g. `v4.2.0`) and select **Create new tag on publish**.
3. Set the title to `v4.2.0`.
4. Click **Generate release notes** to auto-populate the release body from merged PRs.
5. Click **Publish release**.

The tag is created automatically when the release is published — no separate `git tag` step needed. The tag is also what sets the package version at build time.

Publishing the release (not just saving as a draft) triggers two workflows in parallel:

- **publish-distribution.yaml**: builds with `uv build` and publishes to PyPI using the `PYPI_API_TOKEN` secret.
- **publish-documentation.yaml**: builds Sphinx docs and deploys to GitHub Pages.

### 5. Verify the publish workflow

Go to [Workflow runs](https://github.com/smartsheet/smartsheet-python-sdk/actions) and confirm both jobs succeeded.

### 6. Verify on PyPI

```
https://pypi.org/project/smartsheet-python-sdk/4.2.0/
```

The new version should be available immediately after the workflow succeeds.

## Files Changed in Every Release

| File | What changes |
| --- | --- |
| `CHANGELOG.md` | New versioned header inserted below the permanent `Unreleased` placeholder |

## Automation

Publishing is fully automated once the GitHub Release is published:

```
GitHub Release (published) → publish-distribution.yaml → uv build → uv publish → PyPI
                           → publish-documentation.yaml → Sphinx → GitHub Pages
```

The workflow uses a `PYPI_API_TOKEN` GitHub Actions secret — no local credentials needed.

## Troubleshooting

**CI fails on the PR**

Check the `test-build.yaml` run. Common causes: lint failure (`pylint`), test failure on a specific Python version, or a docs build error.

**Publish workflow fails after the release is published**

The tag and GitHub Release already exist — do not delete them. Instead:

1. Investigate the failure in the Actions log (common cause: expired `PYPI_API_TOKEN`).
2. Re-trigger via **Actions → Build and Publish → Re-run jobs** after fixing the root cause.
3. If the root cause requires a code fix, cut a patch release instead.

## Rollback

PyPI does not support deleting released versions. If a bad release ships:

1. Publish a patch release immediately with the fix.
2. Use `pip install smartsheet-python-sdk==4.2.1` in your guidance to users.
3. Optionally yank the bad version via the PyPI UI (yanked versions still exist but are hidden from `pip install` without an explicit version pin).

## Checklist

- [ ] Determined correct semver bump
- [ ] `CHANGELOG.md` versioned header inserted below the permanent `Unreleased` placeholder
- [ ] PR title: `Prepare for release vX.X.X`
- [ ] CI passes on the PR
- [ ] PR merged to `mainline`
- [ ] GitHub Release created: tag `vX.X.X` set to **Create new tag on publish**, release notes generated via "Generate release notes" button, **published** (not draft)
- [ ] `publish-distribution` and `publish-documentation` workflow jobs verified as succeeded
- [ ] Version confirmed on PyPI: `https://pypi.org/project/smartsheet-python-sdk/X.X.X/`
