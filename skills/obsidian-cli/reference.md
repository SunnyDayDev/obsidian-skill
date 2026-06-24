# Obsidian CLI — full command reference

Companion to [SKILL.md](SKILL.md). This is the complete command catalog,
condensed from the official docs at <https://obsidian.md/help/cli>. Always honor
the safety rules in SKILL.md §8 — several commands here are destructive or
developer-only and must not be run unless the user explicitly asks.

## Conventions

- Invocation: `obsidian <command> param=value`. Quote values with spaces;
  encode newlines/tabs as `\n` / `\t`.
- Global: `--copy` copies output to the clipboard.
- Vault targeting: `vault=<name|id>` as the **first** parameter.
- File targeting: `file=<name>` (wikilink resolution) or `path=<path>` (exact
  from vault root); defaults to the active file.
- Run `obsidian` with no command for an interactive TUI (history, `Ctrl+R`
  reverse search, autocomplete).

## General

| Command | Purpose |
| --- | --- |
| `help` | List commands / show help for one |
| `version` | Show Obsidian version |
| `reload` | Reload the app window |
| `restart` | Restart the app |

## Daily notes

| Command | Purpose |
| --- | --- |
| `daily` | Open today's daily note |
| `daily:read` | Read its contents |
| `daily:append content="<text>"` | Append to it |
| `daily:prepend content="<text>"` | Prepend to it |
| `daily:path` | Print its expected path |

## Files & folders

| Command | Purpose |
| --- | --- |
| `create name=<name> content=<text> template=<name> open overwrite newtab` | Create a file |
| `read file=<name> path=<path>` | Read contents |
| `open file=<name> newtab` | Open a file |
| `append file=<name> content=<text> inline` | Append content |
| `prepend file=<name> content=<text> inline` | Prepend content |
| `move file=<name> to=<path>` | Move/rename, updating internal links |
| `rename file=<name> name=<name>` | Rename |
| `delete file=<name> permanent` | Delete (trash by default; `permanent` skips trash) |
| `files folder=<path> ext=<ext> total` | List files |
| `folders folder=<path> total` | List folders |
| `file path=<path>` | File info |
| `folder path=<path> info=files\|folders\|size` | Folder info |

> ⚠️ `delete ... permanent` and `create ... overwrite` are destructive — confirm first.

## Search & navigation

| Command | Purpose |
| --- | --- |
| `search query=<text> path=<folder> limit=<n> case total` | Search the vault |
| `search:context query=<text>` | Search with grep-style match lines |
| `search:open query=<text>` | Open the search view |
| `random folder=<path> newtab` | Open a random note |
| `random:read folder=<path>` | Read a random note |

## Links & structure

| Command | Purpose |
| --- | --- |
| `backlinks file=<name> counts total format=json\|tsv\|csv` | Incoming links |
| `links file=<name> total` | Outgoing links |
| `unresolved total counts verbose` | Unresolved links |
| `orphans total` | Files with no incoming links |
| `deadends total` | Files with no outgoing links |
| `outline file=<name> format=tree\|md\|json total` | Heading outline |

## Tags & properties

| Command | Purpose |
| --- | --- |
| `tags file=<name> sort=count total counts active` | List tags |
| `tag name=<tag> total verbose` | Tag info |
| `properties file=<name> name=<name> count sort=count format=yaml\|json\|tsv total counts active` | List properties |
| `property:set name=<name> value=<value> type=text\|list\|number\|checkbox\|date\|datetime` | Set a property |
| `property:remove name=<name>` | Remove a property |
| `property:read name=<name>` | Read a property |
| `aliases file=<name> total verbose active` | List aliases |

## Tasks

| Command | Purpose |
| --- | --- |
| `tasks file=<name> status="<char>" total done todo verbose daily` | List tasks |
| `task ref=<path:line> file=<name> line=<n> status="<char>" toggle daily done todo` | Show/update a task |

## Templates

| Command | Purpose |
| --- | --- |
| `templates total` | List templates |
| `template:read name=<name> title=<title> resolve` | Read a template |
| `template:insert name=<name>` | Insert into the active file |

## Vault & misc

| Command | Purpose |
| --- | --- |
| `vault info=name\|path\|files\|folders\|size` | Vault info |
| `vaults total verbose` | List vaults |
| `commands filter=<prefix>` | List command IDs |
| `command id=<id>` | Execute a command by ID |
| `hotkeys total verbose format=json\|tsv\|csv` | List hotkeys |
| `bookmarks total verbose format=json\|tsv\|csv` | List bookmarks |
| `bookmark file=<path> subpath=<subpath> folder=<path> search=<query> url=<url> title=<title>` | Add a bookmark |
| `wordcount file=<name> words characters` | Count words/characters |
| `web url=<url> newtab` | Open a URL in the web viewer |
| `unique name=<text> content=<text> paneType=tab\|split\|window open` | Create a unique (timestamped) note |
| `recents total` | List recent files |

## Workspaces & tabs

| Command | Purpose |
| --- | --- |
| `workspace ids` | Show the workspace tree |
| `workspaces total` | List saved workspaces |
| `workspace:save name=<name>` | Save the layout |
| `workspace:load name=<name>` | Load a workspace |
| `workspace:delete name=<name>` | Delete a workspace |
| `tabs ids` | List open tabs |
| `tab:open group=<id> file=<path> view=<type>` | Open a tab |

## Bases

| Command | Purpose |
| --- | --- |
| `bases` | List `.base` files |
| `base:views` | List views in a base |
| `base:create file=<name> view=<name> name=<name> content=<text> open newtab` | Create a base item |
| `base:query file=<name> view=<name> format=json\|csv\|tsv\|md\|paths` | Query a base |

## File history & sync

| Command | Purpose |
| --- | --- |
| `diff file=<name> from=<n> to=<n> filter=local\|sync` | Compare versions |
| `history file=<name>` | List local versions |
| `history:read file=<name> version=<n>` | Read a version |
| `history:restore file=<name> version=<n>` | Restore a version |
| `history:open file=<name>` | Open the recovery UI |
| `sync on\|off` · `sync:status` | Pause/resume sync · status |
| `sync:history` · `sync:read` · `sync:restore` · `sync:deleted` | Sync version operations |

## Publishing

`publish:site` · `publish:list` · `publish:status` · `publish:add file=<name>` ·
`publish:remove file=<name>` · `publish:open file=<name>`.

> ⚠️ Publishing changes what is publicly visible — only on explicit request.

## Plugins, themes & snippets — explicit request only

These modify the user's Obsidian setup. **Do not run unless the user explicitly
asks for the specific action.**

- Plugins: `plugins` · `plugins:enabled` · `plugin id=<id>` ·
  `plugin:enable` · `plugin:disable` · `plugin:install id=<id> enable` ·
  `plugin:uninstall` · `plugin:reload` · `plugins:restrict on|off`
- Themes: `themes` · `theme name=<name>` · `theme:set` · `theme:install` ·
  `theme:uninstall`
- Snippets: `snippets` · `snippets:enabled` · `snippet:enable` ·
  `snippet:disable`

## Developer commands — do not use unless explicitly asked

`devtools` · `dev:debug` · `dev:cdp` · `dev:errors` · `dev:screenshot` ·
`dev:console` · `dev:css` · `dev:dom` · `dev:mobile` · **`eval code=<javascript>`**.

> 🚫 `eval` executes arbitrary JavaScript and `dev:*` are debugging tools. They
> are powerful and unsafe for routine use — never invoke them to satisfy an
> ordinary notes request.
