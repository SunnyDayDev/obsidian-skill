# obsidian-cli-skill Specification

## Purpose

Define the behavior of the Obsidian CLI skill: how it discovers and validates the `obsidian` command-line interface, targets vaults and files, reads and edits notes, manages daily notes, metadata, links, and tasks, and how it stays safe by default by requiring confirmation for destructive actions and keeping restricted commands off unless explicitly requested.

## Requirements

### Requirement: CLI discovery and precondition checks
The skill SHALL verify that the `obsidian` CLI is available and usable before running operations, and SHALL return actionable guidance when a precondition is unmet instead of failing opaquely.

#### Scenario: CLI is available
- **WHEN** the skill is invoked and `obsidian` is on `PATH` with a running Obsidian app
- **THEN** the skill proceeds to run the requested command

#### Scenario: CLI is not installed or not registered
- **WHEN** the `obsidian` binary is not found on `PATH`
- **THEN** the skill SHALL stop and instruct the user to update to Obsidian 1.12.7+ and enable Settings → General → "Command line interface"

#### Scenario: Obsidian app is not running
- **WHEN** the CLI returns an error indicating no running app instance
- **THEN** the skill SHALL instruct the user to launch the Obsidian desktop app before retrying

### Requirement: Vault and file targeting
The skill SHALL target the correct vault and file using the CLI's `vault=`, `file=`, and `path=` parameters, defaulting to the active vault and active file when the user does not specify one.

#### Scenario: Multiple vaults are present
- **WHEN** more than one vault exists and the user names a specific vault
- **THEN** the skill SHALL pass `vault=<name>` as the first parameter before the command

#### Scenario: Target a note by wikilink name
- **WHEN** the user references a note by its name or title
- **THEN** the skill SHALL use `file=<name>` so the CLI resolves it via wikilink logic

#### Scenario: Target a note by exact path
- **WHEN** the user references a note by its path from the vault root
- **THEN** the skill SHALL use `path=<path>` rather than `file=`

### Requirement: Reading notes and inspecting vault structure
The skill SHALL read note contents and enumerate vault structure using non-mutating commands.

#### Scenario: Read a note
- **WHEN** the user asks for the contents of a note
- **THEN** the skill SHALL run `read file=<name>` (or `path=<path>`) and return the contents

#### Scenario: List files in a folder
- **WHEN** the user asks what notes exist in a folder
- **THEN** the skill SHALL run `files folder=<path>` and report the results

#### Scenario: Search the vault
- **WHEN** the user asks to find notes matching text
- **THEN** the skill SHALL run `search query=<text>` (optionally with `path=`, `limit=`) and may use `search:context` for grep-style match lines

### Requirement: Creating and editing notes
The skill SHALL create and edit notes using `create`, `append`, `prepend`, `move`, and `rename`, quoting values that contain spaces and encoding newlines as `\n`.

#### Scenario: Create a new note
- **WHEN** the user asks to create a note with content
- **THEN** the skill SHALL run `create name=<name> content="<text>"` and SHALL NOT pass `overwrite` unless the user has approved replacing an existing file

#### Scenario: Append content to a note
- **WHEN** the user asks to add content to the end of an existing note
- **THEN** the skill SHALL run `append file=<name> content="<text>"`

#### Scenario: Multiline content
- **WHEN** the content spans multiple lines
- **THEN** the skill SHALL encode line breaks as `\n` within the quoted `content` value

### Requirement: Daily notes workflow
The skill SHALL support daily-note operations using the `daily` command family.

#### Scenario: Append to today's daily note
- **WHEN** the user asks to log something to today's daily note
- **THEN** the skill SHALL run `daily:append content="<text>"`

#### Scenario: Read today's daily note
- **WHEN** the user asks what is in today's daily note
- **THEN** the skill SHALL run `daily:read`

### Requirement: Metadata operations for tags and properties
The skill SHALL read and edit note metadata using the `tags`, `property:*`, and `aliases` command families.

#### Scenario: Set a frontmatter property
- **WHEN** the user asks to set a property on a note
- **THEN** the skill SHALL run `property:set name=<name> value=<value> type=<type>` with an appropriate `type`

#### Scenario: List tags
- **WHEN** the user asks which tags a note or vault uses
- **THEN** the skill SHALL run `tags` (optionally `file=<name>`) and report them

### Requirement: Links and graph navigation
The skill SHALL traverse the vault graph using `backlinks`, `links`, `outline`, and `orphans`.

#### Scenario: List backlinks
- **WHEN** the user asks what links to a note
- **THEN** the skill SHALL run `backlinks file=<name>` and may request `format=json` for structured output

#### Scenario: Show a note's outline
- **WHEN** the user asks for the heading structure of a note
- **THEN** the skill SHALL run `outline file=<name>`

### Requirement: Task management
The skill SHALL list and toggle Markdown tasks using the `tasks` and `task` commands.

#### Scenario: List open tasks
- **WHEN** the user asks for outstanding tasks in a note
- **THEN** the skill SHALL run `tasks file=<name> todo`

#### Scenario: Toggle a task
- **WHEN** the user asks to complete a specific task
- **THEN** the skill SHALL run `task ref=<path:line> toggle` (or `done`) after identifying the correct line

### Requirement: Safe-by-default handling of destructive operations
The skill SHALL treat delete, overwrite, move, and rename as actions that require explicit user confirmation, SHALL prefer trash over permanent deletion, and SHALL read existing content before overwriting it.

#### Scenario: Delete a note
- **WHEN** the user asks to delete a note
- **THEN** the skill SHALL run `delete file=<name>` (trash) and SHALL NOT add `permanent` unless the user explicitly requested permanent deletion

#### Scenario: Overwrite an existing note
- **WHEN** creating a note whose name already exists
- **THEN** the skill SHALL confirm with the user before passing `overwrite`, after reading the existing content

#### Scenario: Bulk or irreversible change
- **WHEN** an operation affects multiple files or cannot be easily undone
- **THEN** the skill SHALL summarize the planned effect and ask for confirmation before executing

### Requirement: Restricted commands are off by default
The skill SHALL NOT invoke `eval`, the `dev:*` developer commands, or plugin/theme/snippet management commands unless the user explicitly asks for that action.

#### Scenario: Routine note request never escalates
- **WHEN** the user asks for an ordinary note, search, or metadata operation
- **THEN** the skill SHALL NOT run `eval`, `dev:*`, `plugin:*`, or `theme:*` commands

#### Scenario: Explicit plugin management request
- **WHEN** the user explicitly asks to enable or install a specific plugin
- **THEN** the skill MAY run the corresponding `plugin:*` command after confirming the action

### Requirement: Skill triggering on Obsidian intent
The skill's description SHALL cause Claude Code to invoke it when the user references Obsidian, a vault, daily notes, or note operations expressed in natural language.

#### Scenario: Natural-language note request
- **WHEN** the user says something like "add a note to my Obsidian vault" or "search my vault for X"
- **THEN** Claude Code SHALL select and run this skill
