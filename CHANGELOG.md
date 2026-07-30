# Changelog

All notable changes to the Amazon BR-163 PyEO repository are documented in this file.

The format is based on the principles of Keep a Changelog and records repository changes by released version. Entries describe completed work only and are not intended to document planned or proposed features.

The repository records the development and validation of a Windows-adapted PyEO workflow for Sentinel-2 forest-clearing detection within the Amazon BR-163 pilot area.

## [Unreleased]

No unreleased changes are currently documented.

## [1.1.0] - 2026-07-30

### Added

- Configuration Guide for installing and configuring the project on another computer.
- Local Path Customization Guide identifying machine-specific and validated configuration values.
- Non-destructive configuration validator (`scripts/verify_configuration.py`).
- Portable local configuration template (`amazon_br163_pyeo_local.template.ini`).
- Local configuration generator (`scripts/create_local_configuration.py`).

### Changed

- Updated the README with configuration, path-customization, validation, and local-generation guidance.
- Improved repository onboarding for installation on different Windows computers.
- Separated the validated project configuration from generated local machine configuration.

### Validation

- Configuration validator successfully validates repository structure, configuration parsing, required files, required directories, and processing-stage safety.
- Local configuration generator successfully creates a machine-specific configuration while preserving the validated Version 1.0 configuration.
- Local configuration generation automatically invokes the configuration validator, and the generated configuration passes all validation checks.
- Generated local configuration (`00_admin/amazon_br163_local.ini`) remains excluded from version control through `.gitignore`.

## [1.0] - 2026-07-30

### Added

- Windows-compatible implementation of the PyEO forest-change workflow.
- Copernicus Data Space Ecosystem integration for Sentinel-2 imagery access.
- Sentinel-2 baseline-composite generation workflow.
- Monitoring-period image processing and classification workflow.
- ExtraTrees model training and validation notebooks.
- Binary land-cover classification using:
  - Forest = 1
  - Clearing = 2
- Raster change-detection processing for forest-to-clearing transitions.
- Change-polygon vectorisation.
- Administrative enrichment using Brazil ADM1 boundaries.
- Structured input, raster, classification, change, vector, and repository quality-assurance checks.
- Project configuration through `00_admin/amazon_br163_working.ini`.
- Environment and source-provenance records.
- Repository README and MIT License.

### Changed

- Adapted the PyEO workflow for execution in a Windows and Conda-managed environment.
- Updated notebook paths to use the Amazon BR-163 project directory structure.
- Replaced hard-coded development paths with project-relative or configuration-controlled paths where applicable.
- Renamed the model installation notebook to `01_train_model_installation_validation.ipynb`.
- Separated source materials, working data, generated outputs, documentation, and runtime logs into defined repository directories.
- Updated notebook stage controls so disabled processing stages skip without modifying existing outputs.
- Corrected notebook configuration access to use the configured `bands` value.
- Consolidated the operational change-detection workflow into the active `03_detect_change_working.ipynb` notebook.

### Fixed

- Resolved Windows-specific workflow compatibility issues.
- Corrected stage-skipping behavior in the change-detection notebook.
- Corrected a configuration-key error involving band definitions.
- Removed obsolete temporary recovery cells from the operational notebook.
- Recovered vectorisation after earlier execution failures.
- Corrected administrative enrichment so all validated output polygons receive an administrative-area assignment.
- Removed hard-coded administrative-boundary references from the active workflow.
- Removed temporary diagnostics, development backups, and runtime artifacts from the active repository structure.

### Validated

- Cloud masking completed successfully.
- Radiometric-offset handling completed successfully.
- Baseline composite generation completed successfully.
- Forest and clearing classification completed successfully.
- Raster change detection completed successfully.
- Change-polygon vectorisation completed successfully.
- Administrative enrichment completed successfully.
- Validation-safe notebook execution reached the expected processing end.
- Final enriched vector output contains:
  - 729,869 polygons
  - 32 attributes
  - EPSG:32721
  - 100% administrative-area assignment
- Operational workflow validated for Sentinel-2 tile `21MYM`.
- Baseline period validated for 01 July 2024 through 30 September 2024.
- Monitoring period validated for 01 July 2025 through 30 September 2025.

### Repository

- Initialized Git version control.
- Created the `docs/repository-identity` documentation branch.
- Added repository exclusions for generated imagery, raster products, vector products, logs, credentials, and temporary files.
- Preserved active notebooks, configuration, model artifacts, training inputs, lightweight reference data, and documentation.
- Moved the successful development notebook backup outside the active repository.
- Created the project README.
- Added the MIT License.
- Documented repository structure, installation, workflow order, outputs, quality assurance, known limitations, and future roadmap.
