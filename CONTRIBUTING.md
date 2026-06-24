# Contributing

Thanks for your interest in improving the Obsidian CLI plugin! This project uses
a lightweight **GitFlow** model and validates every change in CI.

## Branching model (GitFlow)

- **`main`** — stable, released code only. Protected; never committed to directly.
- **`develop`** — integration branch; the base for all day-to-day work.
- **`feature/*`** — short-lived branches for a single change, cut from `develop`.

```
feature/my-change  ──PR──▶  develop  ──release PR──▶  main  ──tag──▶  vX.Y.Z
```

### Workflow

1. Branch from `develop`:
   ```bash
   git switch develop && git pull
   git switch -c feature/short-description
   ```
2. Make your change and validate locally (see below).
3. Open a pull request **into `develop`**. CI must pass.
4. Releases are promoted from `develop` to `main` via a reviewed release PR and
   tagged with the semantic version.

## Review policy

For the current single-maintainer phase, **`main` does not require a mandatory
approving review**. Branch protection still enforces that every change reaches
`main` through a **pull request** with **passing CI** and **linear history** —
direct pushes to `main` are rejected. A required-review rule may be enabled
later once there are multiple maintainers.

## Branch protection (maintainers)

`main` protection is reproducible from [`docs/branch-protection.json`](docs/branch-protection.json).
To (re)apply it:

```bash
gh api --method PUT repos/SunnyDayDev/obsidian-skill/branches/main/protection \
  --input docs/branch-protection.json
```

This requires a pull request, a passing `validate` check, and linear history;
blocks direct pushes and force-pushes; and applies to admins too
(`enforce_admins`). It intentionally sets `required_approving_review_count: 0`
(no mandatory review) for the current single-maintainer phase.

## Validate locally

Before opening a PR, run the same checks CI runs:

```bash
# Official plugin/skill/manifest validation
claude plugin validate . --strict

# Manifests are well-formed JSON
jq empty .claude-plugin/plugin.json
jq empty .claude-plugin/marketplace.json
```

## Versioning & changelog

This project follows [Semantic Versioning](https://semver.org/). When your
change affects the skill or packaging, bump `version` in both
`.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, and add an
entry under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).

## Scope & safety

The skill is **safe by default**. When editing it, preserve the safety rules:
prefer trashing over permanent deletion, read before overwriting, confirm bulk
or irreversible actions, and keep developer/`eval`/plugin-management commands
off the default path. New behaviors should map to a requirement in the
`openspec/` specs.
