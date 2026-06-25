## Why

Obsidian 1.12.7+ ships a powerful `obsidian` command-line interface that can drive a running vault (create/read/search notes, manage daily notes, edit frontmatter, toggle tasks, traverse links). Claude Code has no built-in knowledge of this CLI, so users must explain the command syntax every time. Packaging that knowledge as an installable Claude Code Skill — and distributing it as a plugin via a governed public GitHub repo — turns Obsidian into a first-class, safe-by-default surface that Claude Code can operate on demand.

## What Changes

- Add a Claude Code **Skill** (`SKILL.md` + reference docs) that teaches Claude Code how to detect, target, and drive the `obsidian` CLI for common knowledge-management workflows (notes CRUD, search, daily notes, links/backlinks, tags/properties, tasks, listing).
- Establish **safe-by-default operating rules** in the skill: trash over permanent delete, confirm overwrites and bulk/destructive actions, never run `eval`/`dev:*`/plugin-management commands unless explicitly asked, surface dry-run/read-first patterns.
- Package the skill as a distributable **Claude Code plugin** (plugin manifest + marketplace entry) so users can install it with one command.
- Create a **public GitHub repository** (`obsidian-skill`) to host and distribute the plugin, with README, LICENSE, and contribution docs.
- Configure **GitFlow** (`main` + `develop` + feature branches) with **`main` branch protection** (required PR review, required status checks, linear history / no direct pushes) and a CI workflow that validates the skill/plugin on pull requests.

## Capabilities

### New Capabilities
- `obsidian-cli-skill`: The skill behavior — how Claude Code discovers the CLI, targets vaults/files, performs note and metadata operations, and enforces safe-by-default guardrails.
- `plugin-packaging`: The distributable plugin format — manifest, marketplace entry, versioning, and install/update instructions.
- `repository-governance`: The public GitHub repo, GitFlow branching model, `main` branch protection rules, and CI validation on pull requests.

### Modified Capabilities
<!-- None — this is a greenfield project with no existing specs. -->

## Impact

- **New repository**: public GitHub repo `obsidian-skill` (owner to be confirmed at apply time).
- **New files**: `skills/obsidian-cli/SKILL.md` and reference docs; `.claude-plugin/plugin.json` (or equivalent manifest) and `marketplace.json`; `README.md`, `LICENSE`, `CONTRIBUTING.md`; `.github/workflows/*.yml` CI.
- **External systems**: GitHub (repo creation + branch protection via `gh`/API), requires an authenticated GitHub account with admin rights on the repo.
- **Runtime dependency**: end users need Obsidian 1.12.7+ with the CLI enabled and a running app instance; the skill targets the `obsidian` binary on `PATH`.
- **No application code changes** — this is documentation, packaging, and repo governance, not a code library.
