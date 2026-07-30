# Path Customization Guide

## Purpose

This guide explains which configuration values should be customised when installing the Amazon BR-163 PyEO workflow on a different computer.

The validated Version 1.0 workflow contains machine-specific paths that were intentionally preserved to document the validated processing environment.

This guide identifies which values should be changed and which should remain unchanged.

---

## Configuration Philosophy

The project separates configuration into three categories:

| Category | Description |
|----------|-------------|
| Validated configuration | Values used to produce the validated Version 1.0 workflow. |
| User-specific configuration | Values that depend on the local computer. |
| Project configuration | Values that normally remain unchanged between installations. |

---

## Path Customization Matrix

| Configuration Item | Validated Example | Change Required | Notes |
|--------------------|-------------------|-----------------|-------|
| `model` | `05_model/amazon_forest_clearing_extratrees.pkl` | No | Replace only when intentionally using a different trained model. |
| `pyeo_dir` | `C:\GIS\src\pyeo` | Yes | Point to the local PyEO source checkout. |
| `tile_dir` | `C:\GIS\data\Amazon_BR163_PyEO\tile_data` | Yes | Local location for downloaded Sentinel-2 imagery. |
| `integrated_dir` | `08_change/integrated` | Usually No | Leave unchanged unless restructuring the repository. |
| `roi_dir` | `01_roi/pilot` | Usually No | Repository-relative location for the pilot ROI. |
| `geometry_dir` | `02_reference` | Usually No | Repository-relative location for administrative boundaries. |
| `log_dir` | `C:\GIS\logs` | Yes | Local log directory. |
| `credentials_path` | `C:\GIS\secrets\pyeo_cdse.ini` | Yes | Credentials must remain outside the repository. |
| `conda_directory` | `C:\Users\<user>\miniconda3` | Yes | Local Miniconda installation directory. |
| `conda_env_name` | `pyeo_env` | Usually No | Keep unless intentionally using a differently named environment. |

---

## Values That Normally Should Not Change

The following values are part of the validated workflow and should normally remain unchanged:

- Coordinate reference system.
- Class labels.
- Binary class values.
- Change-detection classes.
- Band order.
- Output resolution.
- Processing stage logic.

---

## Credentials

Never commit:

- usernames;
- passwords;
- API tokens;
- authentication keys;
- credential files.

Only the path to the credential file should appear in the configuration.

---

## Before Running the Workflow

Confirm that:

- every customised path exists;
- the Conda environment can be activated;
- the credential file exists;
- the PyEO source directory exists;
- the model file exists;
- the selected processing stage is enabled.

---

## Relationship to Other Documentation

This guide should be read together with:

- `README.md`
- `11_documentation/Configuration_Guide.md`
- `00_admin/amazon_br163_working.ini`
- `00_starting_files/templates/amazon_br163_pyeo_DO_NOT_RUN_UNTIL_EDITED.ini`

---

## Version History

### Version 1.1

Introduced to document which configuration values are installation-specific and which form part of the validated workflow.