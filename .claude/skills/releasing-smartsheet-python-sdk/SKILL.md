---
name: releasing-smartsheet-python-sdk
description: Use when cutting a new release of the Smartsheet Python SDK — changelog update, tag, and GitHub Release
---

# Release

## Overview

Skill for releasing a new version of the Smartsheet Python SDK.

**Full procedure:** Read `RELEASE.md` in the repository root before taking any action. It is the single source of truth for every step, decision rule, and checklist item.

## When to Use

Use when:
- User asks to cut a release or bump the version
- It's time to ship accumulated changes from `mainline`
- A hotfix needs to be published urgently

Do NOT use for:
- Adding features or fixing bugs (those are separate PRs merged first)
- Updating CI or tooling without a version change

## Workflow Summary

```
mainline (green) → decide version → "Prepare for release" PR (CHANGELOG only) → merge → GitHub Release (creates tag + sets version) → PyPI publish (auto)
```

Full details for every step are in `RELEASE.md`.

## Confirmation Gates

**Before committing or pushing anything:** confirm the target version and branch name with the user.

**Before instructing the user to click "Publish release":** confirm they are ready — publishing is the point of no return that triggers PyPI publication and sets the package version via the git tag.
