## ADDED Requirements

### Requirement: Public repository with baseline documentation
A public GitHub repository named `obsidian-skill` SHALL host the plugin and SHALL include a README, an open-source LICENSE, and a CONTRIBUTING guide.

#### Scenario: Visitor opens the repository
- **WHEN** anyone visits the repository
- **THEN** they SHALL see a README describing the plugin, a LICENSE file, and contribution guidance

### Requirement: GitFlow branching model
The repository SHALL use a GitFlow branching model with a stable `main` branch, an integration `develop` branch, and short-lived `feature/*` branches; released code SHALL reach `main` only through merges, not direct commits.

#### Scenario: Starting new work
- **WHEN** a contributor begins a new feature
- **THEN** they SHALL branch from `develop` using a `feature/*` branch and open a pull request back into `develop`

#### Scenario: Promoting to a release
- **WHEN** `develop` is ready to ship
- **THEN** the changes SHALL be merged into `main` via a reviewed pull request and tagged as a release

### Requirement: Protected main branch
The `main` branch SHALL be protected so that direct pushes are rejected, pull requests require at least one approving review, required status checks must pass before merge, and history remains linear.

#### Scenario: Direct push to main is blocked
- **WHEN** anyone attempts to push commits directly to `main`
- **THEN** the push SHALL be rejected by branch protection

#### Scenario: Merge requires review and passing checks
- **WHEN** a pull request targets `main` without an approving review or with failing required checks
- **THEN** the pull request SHALL NOT be mergeable until both conditions are satisfied

### Requirement: Continuous integration on pull requests
A CI workflow SHALL run on pull requests targeting `develop` and `main` and SHALL validate the skill and plugin structure (e.g. manifest JSON validity and skill front-matter), reporting status back to the pull request.

#### Scenario: CI runs on a pull request
- **WHEN** a pull request is opened or updated
- **THEN** the CI workflow SHALL execute the validation checks and report pass/fail as a required status check

### Requirement: Tagged releases with a changelog
Releases SHALL be cut from `main`, tagged with the semantic version, and recorded in a changelog so users can track what changed.

#### Scenario: Cutting a release
- **WHEN** a release is published from `main`
- **THEN** a version tag SHALL be created and the changelog SHALL list the user-visible changes
