## Context

Obsidian 1.12.7+ ships an `obsidian` CLI that drives a running vault through a large, parameterized command surface (`create`, `read`, `search`, `daily:*`, `backlinks`, `property:set`, `tasks`, and developer escape-hatches like `eval` / `dev:*`). We want Claude Code to operate this CLI safely and idiomatically, packaged as an installable plugin and distributed from a governed public GitHub repo (`obsidian-skill`).

This is greenfield: no existing specs, code, or repo. Three concerns are in play — skill behavior, plugin packaging, and repository governance — so a short design pins down structure and naming before implementation. Plugin/skill/marketplace schemas were confirmed against the current Claude Code plugin reference docs.

## Goals / Non-Goals

**Goals:**
- A lean, safe-by-default Skill that wraps the high-value Obsidian CLI workflows (notes CRUD, search, daily notes, links/backlinks, tags/properties, tasks, listing).
- One-command install: the public repo is its own plugin marketplace, so users run `/plugin marketplace add <owner>/obsidian-skill` then `/plugin install obsidian-cli@obsidian-skill`.
- A governed repo: GitFlow (`main`/`develop`/`feature/*`), protected `main`, and CI that validates the plugin on every PR.

**Non-Goals:**
- Not wrapping 100% of the CLI. Developer/escape-hatch commands (`eval`, `dev:*`), and niche families (`publish:*`, `sync:*`, `bases`, `workspace:*`) are intentionally out of the v1 happy path; the reference doc may mention them but the skill does not encourage them.
- Not an MCP server — the CLI already exists, so a Skill (instructions + scoped Bash) is the right weight, not a long-running process.
- Not auto-provisioning the user's GitHub account or Obsidian install; the repo owner and `gh` auth are confirmed with the user at apply time.

## Decisions

### D1: Deliver as a Skill, not an MCP server
A Skill is plain Markdown plus scoped `Bash` access to an already-installed binary — no process to host, no protocol layer. An MCP server would re-wrap a CLI that is itself the integration. **Alternative considered:** an MCP server wrapping `obsidian` — rejected as overweight for a local CLI.

### D2: Repo is its own marketplace (single repo)
Ship `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` in one repo, with the marketplace entry using `"source": "./"`. Users add the repo as a marketplace and install the plugin from it — no second repo to maintain. **Alternative considered:** a separate marketplace repo listing the plugin — rejected; unnecessary indirection for a single plugin.

### D3: Skill layout with progressive disclosure
Use `skills/obsidian-cli/SKILL.md` (lean: triggering, preconditions, targeting model, safety rules, the ~10 core command patterns) plus `skills/obsidian-cli/reference.md` (the full command catalog from the Obsidian docs). SKILL.md stays well under the 1,536-char description budget and links to the reference for breadth. **Alternative considered:** a single large SKILL.md — rejected; bloats the always-loaded description and buries the safety rules.

### D4: Naming
Repo `SunnyDayDev/obsidian-skill`; marketplace name `obsidian-skill`; plugin name `obsidian-cli`; skill `name: obsidian-cli`. Install reads cleanly as `/plugin marketplace add SunnyDayDev/obsidian-skill` then `/plugin install obsidian-cli@obsidian-skill`. The repo name follows the user's explicit request.

### D5: Safety model — scoped tools + in-skill guardrails
The skill declares `allowed-tools` scoped to the Obsidian binary (e.g. `Bash(obsidian:*)`) and deliberately does **not** allow-list a path to `eval`/`dev:*`. SKILL.md encodes the guardrails: trash over permanent delete, read-before-overwrite, confirm bulk/irreversible actions, never run `eval`/`dev:*`/`plugin:*`/`theme:*` unless explicitly asked. Because the CLI uses `command param=value` (not flags), allow-patterns are coarse and cannot by themselves block a specific subcommand — so safety is enforced primarily by the skill instructions, with tool-scoping as defense-in-depth. **Alternative considered:** relying on allow-patterns alone — rejected as insufficient given the flat command grammar.

### D6: CI validates with the official tool
The PR workflow runs `claude plugin validate . --strict` (validates `plugin.json`, `marketplace.json`, and skill frontmatter) plus a JSON/YAML lint. This is the required status check on `main`/`develop`. **Alternative considered:** a hand-rolled validator — rejected; the official command tracks schema changes.

### D7: Governance configured via `gh` and documented as code
GitFlow is documented in CONTRIBUTING; `main` protection is applied with `gh api` (or a repository ruleset) requiring PRs, ≥1 approving review, the CI status check, linear history, and no direct pushes. The exact protection payload is checked into docs so it is reproducible. **Alternative considered:** click-ops in the GitHub UI — rejected as non-reproducible.

### D8: MIT license
Permissive and conventional for Claude Code plugins/skills, maximizing adoption. **Alternative considered:** Apache-2.0 — viable, but MIT is lighter-weight for a docs-only plugin.

## Risks / Trade-offs

- **CLI exposes destructive and code-exec commands (`delete permanent`, `eval`, `dev:*`)** → Mitigation: guardrails in SKILL.md (D5), no allow-listed path to escape-hatches, explicit confirmation gates on destructive ops.
- **Coarse `Bash` allow-patterns can't block individual subcommands** → Mitigation: treat tool-scoping as defense-in-depth only; the skill's behavioral rules are the primary control, and they are spec-backed and testable.
- **Single-maintainer review requirement** → A "require 1 approving review" rule cannot be satisfied by the author alone on a solo repo. **Resolved:** v1 protects `main` with required PR + passing CI + linear history and **no** mandatory approving review; review enforcement can be added later if collaborators join.
- **Branch-protection mechanics differ (classic protection vs rulesets; some options gated by org/plan)** → Mitigation: target public-repo-supported settings, document both the `gh api` classic-protection call and a ruleset fallback.
- **Obsidian CLI surface may drift across versions** → Mitigation: pin the documented minimum version (1.12.7+), link to `https://obsidian.md/help/cli`, and keep `reference.md` the single place to update.

## Migration Plan

Greenfield — no data or API migration. Rollout:
1. Scaffold the repo contents locally (skill, manifests, docs, CI).
2. Validate locally with `claude plugin validate . --strict`.
3. `git init`, create `main`, branch `develop`; push to the new public GitHub repo `obsidian-skill` (owner confirmed at apply time).
4. Apply `main` branch protection via `gh api`; set `develop` as the working base.
5. Tag `v1.0.0` from `main`; verify install end-to-end with `/plugin marketplace add` + `/plugin install`.

Rollback: branch protection can be lifted via `gh api`; the repo can be unpublished/deleted; install is reversible with `/plugin uninstall`. No external state is mutated besides the GitHub repo.

## Resolved Decisions

- **GitHub owner**: `SunnyDayDev` — `gh` is authenticated as `SunnyDayDev` with the `repo` scope (sufficient to create the repo and manage `main` branch protection). Repo URL: `https://github.com/SunnyDayDev/obsidian-skill`.
- **Solo-repo review policy**: ship v1 with **no mandatory approving review**. `main` protection requires a pull request, passing CI, and linear history, and blocks direct pushes; review enforcement can be added later if collaborators join.
- **v1 command coverage**: the proposed core families are sufficient — notes CRUD, search, daily, links/backlinks, tags/properties, tasks, and listing in `SKILL.md`; the full catalog lives in `reference.md`.
