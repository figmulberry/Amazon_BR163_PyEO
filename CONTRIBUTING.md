# Contributing

Thank you for your interest in contributing to the Amazon BR-163 PyEO project.

This repository contains a validated Windows adaptation of the PyEO workflow for detecting forest clearing using Sentinel-2 imagery within the Amazon BR-163 pilot area. Contributions should preserve the project's emphasis on reproducibility, validation, and maintainability.

## Guiding Principles

All contributions should:

- Preserve reproducibility.
- Keep changes focused and well documented.
- Avoid introducing unnecessary complexity.
- Maintain consistency across notebooks and documentation.
- Be validated before submission.

## Repository Workflow

The recommended workflow is:

1. Create a dedicated branch for your work.
2. Make focused changes that address a single objective.
3. Validate all affected notebooks or documentation.
4. Review your changes before staging.
5. Run repository quality checks.
6. Commit using a descriptive commit message.
7. Submit the work for review before merging.

## Branch Naming

Use descriptive branch names such as:

- `feature/<feature-name>`
- `fix/<issue-name>`
- `docs/<documentation-topic>`

Examples:

- `feature/improved-validation`
- `fix/windows-path-handling`
- `docs/repository-identity`

## Commit Messages

Use concise commit messages that clearly describe the purpose of the change.

Examples:

```text
docs: update README
docs: add project changelog
fix: correct configuration loading
feat: improve raster validation
```

## Notebook Standards

Operational notebooks should:

- Have one primary purpose.
- Execute from top to bottom without requiring manual intervention.
- Avoid hard-coded local file paths where configuration can be used.
- Remove temporary debugging or recovery cells before committing.
- Be validated after significant modifications.

## Documentation Standards

Documentation should:

- Describe implemented functionality only.
- Keep README, CHANGELOG, and supporting documents consistent.
- Use clear and concise technical language.
- Record completed work rather than planned work.

## Data Management

The repository should **not** contain:

- Downloaded Sentinel-2 imagery.
- Generated composite rasters.
- Generated classification rasters.
- Generated change-detection rasters.
- Generated vector outputs.
- Runtime logs.
- Credentials or authentication files.
- Temporary processing files.

The repository **should** contain:

- Source notebooks.
- Configuration files.
- Documentation.
- Model artifacts.
- Training inputs.
- Lightweight reference datasets.

## Quality Assurance

Before committing:

- Review notebook changes.
- Review documentation changes.
- Run:

```text
git diff --check
git status
```

- Confirm that only the intended files are staged.
- Ensure the repository remains reproducible from the documented workflow.

## Pull Requests

Before requesting a review:

- Verify that the workflow executes successfully where applicable.
- Update documentation if behaviour has changed.
- Ensure generated outputs have not been committed.
- Confirm that commit messages accurately describe the changes.

## Questions

If you are unsure whether a change belongs in the repository, open a discussion before implementing substantial modifications.