# Obsidian CLI — a Claude Code plugin

Operate your [Obsidian](https://obsidian.md) vault directly from
[Claude Code](https://claude.com/claude-code). This plugin ships a single
**Skill** that teaches Claude Code how to drive the official `obsidian`
command-line interface — reading, creating, searching, and organizing notes —
**safely, by default**.

Ask in plain language ("add a note to my vault", "search my Obsidian for X",
"log this to today's daily note", "what links to this note?") and Claude Code
runs the right `obsidian` commands for you.

## What it can do

- **Notes**: read, create, append/prepend, move, rename, delete (to trash)
- **Search & explore**: full-text search, list files/folders, file info
- **Daily notes**: open, read, append, prepend
- **Metadata**: frontmatter properties, tags, aliases
- **Graph**: backlinks, outgoing links, outline, orphans, unresolved links
- **Tasks**: list and toggle Markdown checkboxes

It is **safe by default**: it trashes instead of permanently deleting, reads
before overwriting, confirms bulk or irreversible actions, and never runs
developer / `eval` / plugin-management commands unless you explicitly ask.

## Prerequisites

1. **Obsidian 1.12.7 or newer** (desktop), with the app **running**.
2. **The Obsidian CLI enabled**: in Obsidian, go to
   **Settings → General → "Command line interface"** and follow the prompts to
   register it. This puts an `obsidian` binary on your `PATH`
   (`/usr/local/bin/obsidian` on macOS, `~/.local/bin/obsidian` on Linux,
   a redirector on Windows).
3. Verify it works: `obsidian version`.

See the [official CLI documentation](https://obsidian.md/help/cli) for details.

## Install

In Claude Code, add this repository as a plugin marketplace, then install the
plugin from it:

```
/plugin marketplace add SunnyDayDev/obsidian-skill
/plugin install obsidian-cli@obsidian-skill
```

That's it — ask Claude Code to work with your vault.

## Update

```
/plugin update obsidian-cli@obsidian-skill
```

## Uninstall

```
/plugin uninstall obsidian-cli@obsidian-skill
/plugin marketplace remove obsidian-skill
```

## How it works

The plugin contains one skill, [`skills/obsidian-cli`](skills/obsidian-cli/SKILL.md).
Claude Code loads its description and invokes it whenever your request involves
Obsidian. The skill knows the CLI's targeting model (`vault=`, `file=`,
`path=`), the common command families, and a set of safety rules. The full
command catalog lives in
[`skills/obsidian-cli/reference.md`](skills/obsidian-cli/reference.md).

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for the
GitFlow branching model and how to validate changes locally.

## License

[MIT](LICENSE) © SunnyDayDev
