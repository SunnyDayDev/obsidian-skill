## ADDED Requirements

### Requirement: Valid plugin manifest
The repository SHALL contain a valid Claude Code plugin manifest that declares the plugin name, version, description, and author, and that exposes the Obsidian CLI skill so it is discoverable once installed.

#### Scenario: Manifest is present and well-formed
- **WHEN** the plugin is inspected
- **THEN** a manifest (e.g. `.claude-plugin/plugin.json`) SHALL exist with valid JSON containing at least `name`, `version`, and `description`

#### Scenario: Skill is exposed after install
- **WHEN** a user installs the plugin into Claude Code
- **THEN** the `obsidian-cli` skill SHALL appear in the available skills and be invocable

### Requirement: Marketplace entry for one-command installation
The repository SHALL provide a marketplace manifest so the plugin can be added and installed via Claude Code's plugin marketplace commands directly from the public repo.

#### Scenario: Add marketplace from the repo
- **WHEN** a user runs the marketplace-add command against the repository URL
- **THEN** the plugin SHALL be listed and installable without manual file copying

### Requirement: Semantic versioning
The plugin version SHALL follow semantic versioning (MAJOR.MINOR.PATCH) and SHALL be incremented whenever a release changes the skill or packaging.

#### Scenario: Release bumps the version
- **WHEN** a change to the skill or manifest is released
- **THEN** the manifest `version` SHALL be incremented according to semver and recorded in the changelog

### Requirement: Install, update, and uninstall documentation
The README SHALL document prerequisites and the exact commands to install, update, and uninstall the plugin.

#### Scenario: User follows the README to install
- **WHEN** a user follows the install steps in the README
- **THEN** the plugin SHALL install successfully and the documented prerequisites (Obsidian 1.12.7+ with CLI enabled) SHALL be stated up front
