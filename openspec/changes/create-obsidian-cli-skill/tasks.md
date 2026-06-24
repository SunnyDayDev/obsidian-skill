## 1. Repository scaffolding

- [x] 1.1 Create the repo skeleton: `.claude-plugin/`, `skills/obsidian-cli/`, `.github/workflows/`
- [x] 1.2 Add `README.md` with a one-paragraph description, prerequisites (Obsidian 1.12.7+ with CLI enabled, running app), and placeholders for install/update sections
- [x] 1.3 Add `LICENSE` (MIT) and a `.gitignore`
- [x] 1.4 Add `CONTRIBUTING.md` documenting the GitFlow model (`main`/`develop`/`feature/*`, PRs into `develop`)
- [x] 1.5 Add `CHANGELOG.md` seeded with an `Unreleased` section

## 2. Skill authoring (capability: obsidian-cli-skill)

- [x] 2.1 Write `skills/obsidian-cli/SKILL.md` frontmatter: `name: obsidian-cli`, a trigger-rich `description` (Obsidian/vault/notes intent, under the 1,536-char budget), and `allowed-tools` scoped to the `obsidian` binary
- [x] 2.2 Document CLI discovery and precondition checks (binary on PATH, Obsidian 1.12.7+, running app) with the actionable failure messages
- [x] 2.3 Document the vault/file targeting model (`vault=`, `file=` vs `path=`, active defaults)
- [x] 2.4 Document core read operations (`read`, `files`, `folders`, `search`, `search:context`)
- [x] 2.5 Document core write operations (`create`, `append`, `prepend`, `move`, `rename`) with quoting and `\n` encoding rules
- [x] 2.6 Document daily notes (`daily:*`), metadata (`tags`, `property:*`, `aliases`), links/graph (`backlinks`, `links`, `outline`, `orphans`), and tasks (`tasks`, `task ... toggle`)
- [x] 2.7 Write the safety-by-default section: trash over `permanent`, read-before-overwrite, confirm bulk/irreversible actions, and the restricted-commands rule (never `eval`/`dev:*`/`plugin:*`/`theme:*` unless explicitly asked)
- [x] 2.8 Write `skills/obsidian-cli/reference.md` with the full command catalog (from https://obsidian.md/help/cli) for progressive disclosure
- [x] 2.9 Self-check SKILL.md against every scenario in `specs/obsidian-cli-skill/spec.md`

## 3. Plugin & marketplace packaging (capability: plugin-packaging)

- [x] 3.1 Write `.claude-plugin/plugin.json` (`name: obsidian-cli`, `version: 0.1.0`, `description`, `author`, `homepage`/`repository`, `license: MIT`, `keywords`)
- [x] 3.2 Write `.claude-plugin/marketplace.json` (`name: obsidian-skill`, `owner`, `plugins: [{ name: obsidian-cli, source: "./", description, version }]`)
- [x] 3.3 Fill in the README install/update/uninstall commands (`/plugin marketplace add <owner>/obsidian-skill`, `/plugin install obsidian-cli@obsidian-skill`, `/plugin update ...`, `/plugin uninstall ...`)

## 4. Local validation

- [x] 4.1 Run `claude plugin validate . --strict` and fix any manifest/frontmatter errors
- [ ] 4.2 Manually install the plugin from the local path and confirm the `obsidian-cli` skill is invocable
- [ ] 4.3 Smoke-test a non-destructive command end-to-end (e.g. `read`/`search`) against a real vault

## 5. CI validation (capability: repository-governance)

- [x] 5.1 Add `.github/workflows/ci.yml` that runs on pull requests to `develop` and `main`
- [x] 5.2 CI step: install Claude Code CLI and run `claude plugin validate . --strict`
- [x] 5.3 CI step: lint JSON/YAML (`plugin.json`, `marketplace.json`, SKILL.md frontmatter)
- [x] 5.4 Confirm the workflow's check name so it can be set as a required status check

## 6. GitHub repository, GitFlow & branch protection (capability: repository-governance)

- [x] 6.1 Use confirmed owner `SunnyDayDev` (gh authenticated, `repo` scope) — repo URL `https://github.com/SunnyDayDev/obsidian-skill`
- [x] 6.2 Record the review policy in CONTRIBUTING: **no mandatory approving review** in v1 (`main` requires PR + CI + linear history)
- [x] 6.3 `git init`, commit the scaffold to `main`, create `develop` from `main`
- [x] 6.4 Create the public GitHub repo `obsidian-skill` and push `main` and `develop`
- [x] 6.5 Apply `main` branch protection via `gh api` (require PR, required status check = CI, linear history, block direct pushes; **no required approving review**) and commit the protection payload into the repo docs for reproducibility
- [x] 6.6 Verify protection: a direct push to `main` is rejected and a PR with failing CI cannot merge

## 7. Release

- [x] 7.1 Bump `version` to `1.0.0` in `plugin.json`/`marketplace.json` and finalize the `CHANGELOG.md` entry
- [x] 7.2 Open and merge the release PR into `main`, then tag `v1.0.0`
- [ ] 7.3 Verify end-to-end install from the public repo with `/plugin marketplace add` + `/plugin install` on a clean Claude Code
