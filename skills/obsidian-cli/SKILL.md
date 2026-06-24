---
name: obsidian-cli
description: >-
  Operate the user's Obsidian vault through the `obsidian` command-line
  interface (Obsidian 1.12.7+). Use whenever the user wants to read, create,
  append, search, move, rename, or delete notes; work with their Obsidian vault
  or daily notes; manage frontmatter properties, tags, or aliases; follow
  backlinks and outgoing links or inspect a note's outline; or list and toggle
  Markdown tasks. Safe by default: prefers trashing over permanent deletion,
  reads before overwriting, confirms destructive or bulk actions, and never
  runs developer, eval, or plugin-management commands unless explicitly asked.
allowed-tools: Bash(obsidian:*)
---

# Obsidian CLI

Drive a **running** Obsidian vault through the `obsidian` binary. Commands take
the form `obsidian <command> param=value`. This skill covers the everyday 90%;
the full command catalog is in [reference.md](reference.md).

## 1. Preconditions — check before acting

1. **Binary present:** confirm the CLI is installed with `command -v obsidian`.
   - If missing: tell the user to update to **Obsidian 1.12.7+** and enable
     **Settings → General → "Command line interface"**, then retry. Do not guess
     at an alternate path.
2. **App running:** the CLI controls the live app. If a command reports no
   running instance, ask the user to **launch the Obsidian desktop app**.
3. A quick, harmless probe is `obsidian version`.

## 2. How the CLI works

- **Syntax:** `obsidian <command> param=value`. Quote any value containing
  spaces: `content="hello world"`.
- **Newlines/tabs:** encode as `\n` and `\t` inside quoted values.
- **Output to clipboard:** append `--copy` when the user wants the result copied.
- Prefer **read-only commands first** to confirm state before mutating.

## 3. Targeting the vault and file

- **Vault:** defaults to the active/current-directory vault. To target another,
  pass `vault=<name>` (or `vault=<id>`) **as the first parameter**, before the
  command's own params.
- **File — two ways:**
  - `file=<name>` resolves by Obsidian **wikilink** logic (use when the user
    names a note by title).
  - `path=<path>` is an **exact path from the vault root** (use when the user
    gives a path or you need to disambiguate).
  - With neither, commands act on the **active file**.

## 4. Reading & exploring (non-mutating — safe)

| Goal | Command |
| --- | --- |
| Read a note | `read file=<name>` or `read path=<path>` |
| List files in a folder | `files folder=<path>` (add `ext=md`, `total`) |
| List subfolders | `folders folder=<path>` |
| Full-text search | `search query="<text>"` (add `path=`, `limit=`, `case`) |
| Search with match lines | `search:context query="<text>"` |
| File info | `file path=<path>` |
| Vault info | `vault info=name|path|files|folders|size` |

## 5. Creating & editing notes

| Goal | Command |
| --- | --- |
| Create a note | `create name=<name> content="<text>"` |
| Create from template | `create name=<name> template=<name>` |
| Append to end | `append file=<name> content="<text>"` |
| Prepend to start | `prepend file=<name> content="<text>"` |
| Move / rename (updates links) | `move file=<name> to=<path>` · `rename file=<name> name=<new>` |

- **Never pass `overwrite`** on `create` unless the user has approved replacing
  an existing file — and read the existing content first (see §8).
- Multi-line `content` uses `\n` between lines.

## 6. Daily notes

`daily` (open) · `daily:read` · `daily:append content="<text>"` ·
`daily:prepend content="<text>"` · `daily:path`. Use `daily:append` to log
something to today's note.

## 7. Metadata, links & tasks

- **Properties (frontmatter):** `property:set name=<name> value=<value> type=<text|list|number|checkbox|date|datetime>` · `property:read name=<name>` · `property:remove name=<name>`.
- **Tags / aliases:** `tags` (optionally `file=<name>`, `sort=count`) · `aliases file=<name>`.
- **Graph:** `backlinks file=<name>` (add `format=json` for structured output) · `links file=<name>` · `outline file=<name>` · `orphans` · `unresolved`.
- **Tasks:** `tasks file=<name> todo` (or `done`) to list; `task ref=<path:line> toggle` (or `done`) to complete a specific task after identifying its line.

## 8. Safety rules — always

1. **Destructive actions need explicit confirmation.** Delete, overwrite, move,
   and rename change or remove data — summarize what will happen and confirm
   first.
2. **Trash, don't destroy.** `delete file=<name>` moves to trash. **Only** add
   `permanent` when the user explicitly asks for permanent deletion.
3. **Read before overwrite.** Before `create ... overwrite` or replacing
   content, `read` the existing note so nothing is lost silently.
4. **Bulk / irreversible → confirm.** If an action touches multiple files or is
   hard to undo, describe the scope and get a yes before running it.
5. **Escape-hatch commands are off by default.** Do **not** run `eval`, `dev:*`,
   `plugin:*`, `theme:*`, `snippet:*`, `sync:*`, or `publish:*` unless the user
   explicitly requests that specific action; then confirm before executing.

## 9. Examples

```bash
# "Add a meeting note"
obsidian create name="2026-06-24 Standup" content="## Notes\n- ...\n## Actions\n- [ ] "

# "Search my vault for anything about onboarding"
obsidian search query="onboarding" limit=20

# "Log this to today's daily note"
obsidian daily:append content="Shipped the CLI skill 🎉"

# "What links to the Roadmap note?"
obsidian backlinks file="Roadmap" format=json

# "Mark the second task in Today done" (after reading to find the line)
obsidian task ref="Today.md:14" done

# "Delete the scratch note" → trash, not permanent, after confirming
obsidian delete file="Scratch"
```

For anything beyond the above (publishing, sync, bases, workspaces, themes,
developer tools), consult [reference.md](reference.md) — and remember the
escape-hatch rule in §8.
