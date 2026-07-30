# Configuration Guide

## Purpose

This guide explains how to configure the Amazon BR-163 PyEO project on a new computer.

The validated Version 1.0 workflow was developed and tested on Windows using Miniconda and a local PyEO source checkout. This guide explains how to reproduce that environment while keeping credentials and machine-specific settings outside the repository.

The repository intentionally separates:

- Validated project configuration
- Local machine configuration
- Credentials
- Generated outputs

---

## Repository Structure

The project is organised as follows:

```text
Amazon_BR163_PyEO/
|
+-- .github/
|   +-- ISSUE_TEMPLATE/
|
+-- 00_admin/
|   +-- Active configuration
|   +-- Environment history
|   +-- Provenance records
|
+-- 00_starting_files/
|   +-- Templates
|   +-- Helper scripts
|   +-- Quick-reference commands
|
+-- 01_roi/
|
+-- 02_reference/
|
+-- 03_notebooks/
|
+-- 04_training/
|
+-- 05_model/
|
+-- 06_composites/
|
+-- 06_outputs/
|
+-- 07_classification/
|
+-- 08_change/
|
+-- 09_qgis/
|
+-- 10_exports/
|
+-- 11_documentation/
|
+-- 11_logs/
|
+-- 12_reports/
|
+-- README.md
+-- LICENSE
+-- CHANGELOG.md
+-- CONTRIBUTING.md
+-- CODE_OF_CONDUCT.md
```

---

## Software Requirements

Install the following software before attempting to execute the workflow.

- Git
- Miniconda
- Python
- JupyterLab
- GDAL
- Rasterio
- GeoPandas
- QGIS
- Compatible PyEO source checkout

---

## External Components

The repository intentionally does **not** contain:

- Copernicus Data Space credentials
- Downloaded Sentinel-2 imagery
- SAFE products
- Runtime logs
- Temporary processing outputs
- Complete PyEO source code

These components must be supplied locally.

---

## Configuration Files

### Validated Configuration

```text
00_admin/amazon_br163_working.ini
```

This file represents the validated Version 1.0 workflow configuration used to generate the published outputs.

Only modify this file when intentionally updating the validated workflow.

---

### Configuration Template

```text
00_starting_files/templates/amazon_br163_pyeo_DO_NOT_RUN_UNTIL_EDITED.ini
```

This template is intended for configuring the project on another computer.

Create your own local configuration from this template rather than modifying the validated configuration until you have confirmed your environment is working correctly.

---

## Credentials

Credentials must always remain **outside** the repository.

Recommended location:

```text
C:\GIS\secrets\
```

Do **not** commit:

- usernames
- passwords
- API keys
- authentication tokens
- credential files

---

## Local Machine Configuration

The following values are expected to differ between computers:

- PyEO installation directory
- Conda installation directory
- Conda environment location
- Data storage directory
- Log directory
- Credentials directory

These values should be updated to match the local machine while preserving the remainder of the validated configuration.

---

## Validation Checklist

Before running any notebook, verify the following:

- Git repository cloned successfully.
- PyEO source checkout available.
- Conda environment created.
- Required Python packages installed.
- Credentials configured.
- ROI data present.
- Reference layers available.
- Model file available.
- Only the intended processing stage is enabled.
- Output directories exist.

---

## Troubleshooting

If validation fails:

1. Verify the active Conda environment.
2. Confirm all configured paths exist.
3. Check that credentials are stored outside the repository.
4. Verify the PyEO source checkout.
5. Confirm the required processing stage has been enabled.
6. Review notebook output for validation messages before rerunning.

---

## Version History

### Version 1.1

Introduced a dedicated configuration guide to improve portability and onboarding while preserving the validated Version 1.0 processing workflow.