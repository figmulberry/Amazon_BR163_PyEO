# Amazon BR-163 PyEO

A Windows adaptation of the PyEO forest change detection workflow for monitoring forest clearing within the BR-163 corridor in the Brazilian Amazon.

This repository documents a complete implementation of an operational forest-change monitoring workflow using Sentinel-2 imagery, a validated ExtraTrees classification model, raster change detection, polygon vectorization, administrative enrichment, and structured quality assurance.

## Project Status

**Status:** Functional pilot implementation completed and validated.

Current validated configuration:

- Study area: Amazon BR-163 Pilot
- Sentinel-2 tile: 21MYM
- Baseline period: 01 July 2024 – 30 September 2024
- Monitoring period: 01 July 2025 – 30 September 2025
- Coordinate reference system: EPSG:32721
- Output resolution: 10 metres
- Classification:
  - Forest = 1
  - Clearing = 2

## Key Capabilities

- Windows-compatible PyEO workflow
- Copernicus Data Space integration
- Sentinel-2 preprocessing
- Cloud masking QA
- Composite generation
- Forest / clearing classification
- Change detection
- Raster report generation
- Polygon vectorization
- Administrative enrichment
- Structured quality assurance
- Validation-safe notebook execution


## Repository Structure

```
Amazon_BR163_PyEO
│
├── 00_admin
│   Active configuration, provenance records, and reproducibility information.
│
├── 00_starting_files
│   Templates, helper scripts, command references, and setup material.
│
├── 01_roi
│   Region of interest and Sentinel-2 tile definitions.
│
├── 02_reference
│   Administrative boundaries and project reference datasets.
│
├── 03_notebooks
│   Operational notebooks executed in workflow order.
│
├── 04_training
│   Training and validation polygons.
│
├── 05_model
│   Trained machine-learning model and evaluation outputs.
│
├── 06_composites
│   Generated baseline composites (Git ignored).
│
├── 06_outputs
│   Generated raster outputs (Git ignored).
│
├── 07_classification
│   Generated classification outputs (Git ignored).
│
├── 08_change
│   Generated change-detection products (Git ignored).
│
├── 09_qgis
│   Optional local QGIS project.
│
├── 10_exports
│   Generated export products (Git ignored).
│
├── 11_documentation
│   Extended project documentation.
│
├── 11_logs
│   Runtime logs (Git ignored).
│
├── 12_reports
│   Lightweight reports and summary products.
│
├── README.md
├── LICENSE
└── .gitignore
```

### Repository Philosophy

The repository contains:

- source notebooks;
- configuration;
- training data;
- model;
- documentation;
- lightweight reference layers.

The repository intentionally excludes:

- downloaded Sentinel-2 imagery;
- generated composites;
- classified rasters;
- change rasters;
- enriched vector outputs;
- runtime logs;
- large temporary processing products.

These outputs are regenerated when the workflow is executed.

## Workflow

The operational workflow is designed as a sequence of notebooks. Each notebook performs one major stage of the processing pipeline.

```text
Kernel Test
    │
    ▼
Model Training
    │
    ▼
Model Installation Validation
    │
    ▼
Baseline Composite Generation
    │
    ▼
Monitoring Image Processing
    │
    ▼
Forest / Clearing Classification
    │
    ▼
Change Detection
    │
    ▼
Vectorisation
    │
    ▼
Administrative Enrichment
    │
    ▼
Quality Assurance
```

### Operational Notebook Order

| Step | Notebook | Purpose |
|------|----------|---------|
| 0 | `00_pyeo_kernel_test.ipynb` | Verify that the Python environment, GDAL, and PyEO installation are working correctly. |
| 1 | `01_train_amazon_model.ipynb` | Train and validate the ExtraTrees forest-clearing classification model. |
| 2 | `01_train_model_installation_validation.ipynb` | Confirm that the trained model loads correctly and produces compatible classifications. |
| 3 | `02_make_composite_working.ipynb` | Build the baseline Sentinel-2 composite used as the forest reference. |
| 4 | `03_detect_change_working.ipynb` | Execute monitoring, classification, change detection, vectorisation, administrative enrichment, and quality assurance. |

### Operational Principle

The repository is controlled through the active configuration file:

```
00_admin/amazon_br163_working.ini
```

Only the processing stage intentionally enabled in the INI should execute.

All disabled stages are expected to skip cleanly without modifying existing outputs.

## Installation and Environment

The workflow was developed and validated on Windows using a Conda-managed Python environment.

> **Configuration Guide**
>
> Before configuring the project on a new computer, review the
> [Configuration Guide](11_documentation/Configuration_Guide.md).
>
> The Configuration Guide walks new users through installing the required software, configuring local paths, setting up credentials, validating the environment, and preparing the repository for execution.

> **Local Path Customization Guide**
>
> After reviewing the Configuration Guide, continue with the
> [Path Customization Guide](11_documentation/Path_Customization_Guide.md).
>
> This guide explains which configuration values should be customised for your local installation and which values should remain unchanged to preserve the validated workflow.

### Configuration Validation

Always validate the repository configuration before running any processing notebook.

Run:

```powershell
python scripts/verify_configuration.py
```

A successful validation ends with:

```text
Configuration validation passed.
```

The validator performs non-destructive checks only. It does **not**:

- download imagery;
- execute notebooks;
- modify outputs;
- run the PyEO processing pipeline.

### Local Configuration Generator

Instead of manually editing the validated configuration, generate a local machine-specific configuration:

```powershell
python scripts/create_local_configuration.py
```

The generator:

- creates `00_admin/amazon_br163_local.ini`;
- preserves the validated Version 1.0 configuration;
- automatically validates the generated configuration using `verify_configuration.py`;
- never commits the generated local configuration to Git.

### Software

Install the following software before attempting to run the project:

| Software | Purpose |
|----------|---------|
| Miniconda | Python environment management |
| Python | Runtime environment |
| JupyterLab | Execute operational notebooks |
| GDAL | Raster processing |
| GeoPandas | Vector processing |
| Rasterio | Raster input/output |
| QGIS | Visual review and quality assurance |
| Git | Version control |

### Python Environment

The validated environment is:

```
pyeo_env
```

The repository contains reproducibility information inside:

```
00_admin/
```

including:

- environment_history.yml
- pyeo_source_commit.txt
- cdse_patch_base_commit.txt

### External Dependency

This repository does not include the complete PyEO source code.

The validated implementation expects a compatible PyEO source checkout.

Validated location:

```
C:\GIS\src\pyeo
```

### Active Configuration

The operational workflow is controlled through:

```
00_admin/amazon_br163_working.ini
```

Only the stage intentionally enabled inside this INI should execute.

Disabled stages should skip cleanly.

### Credentials

Copernicus Data Space credentials must be configured locally.

Credential files must never be committed into Git.

Templates are provided inside:

```
00_starting_files/templates/
```

### Generated Data

The following products are intentionally excluded from Git:

- downloaded Sentinel-2 imagery
- SAFE folders
- generated composites
- classified rasters
- change rasters
- generated shapefiles
- runtime logs

These products are regenerated during workflow execution.

## Outputs

The workflow produces several categories of outputs.

### Model Outputs

Location:

```
05_model/
```

Examples include:

- trained ExtraTrees model
- confusion matrices
- classification metrics
- validation reports
- model metadata

These files document the performance of the classification model used throughout the workflow.

---

### Composite Outputs

Location:

```
06_composites/
```

Generated during baseline processing.

Typical products include:

- cloud-free Sentinel-2 composite
- auxiliary raster files

These products are regenerated whenever the baseline composite is rebuilt.

---

### Classification Outputs

Location:

```
07_classification/
```

Generated during image classification.

Typical outputs include:

- classified raster
- probability products (when enabled)

---

### Change Detection Outputs

Location:

```
08_change/
```

Generated during change detection.

Typical outputs include:

- raster change report
- vectorised change polygons
- zonal statistics
- administrative enrichment

The validated pilot implementation produced an enriched vector dataset containing:

- 729,869 polygons
- 32 attributes
- EPSG:32721
- 100% administrative match coverage

---

### Reports

Location:

```
12_reports/
```

Contains lightweight project summaries, including:

- classification summary
- area statistics

---

### Runtime Logs

Location:

```
11_logs/
```

Runtime logs are generated during execution.

These files assist troubleshooting and validation but are intentionally excluded from Git.

---

### Version-Control Policy

The repository tracks:

- notebooks
- configuration
- model
- documentation
- lightweight reference data

The repository does **not** track:

- downloaded Sentinel-2 imagery
- generated raster products
- generated vector products
- temporary processing files
- runtime logs

Operational outputs are regenerated by executing the workflow.

## Quality Assurance

Quality assurance is integrated throughout the workflow rather than performed only at the end.

Each operational stage includes validation before processing proceeds.

### Input Validation

Examples include:

- Sentinel-2 SAFE folder verification
- required file existence checks
- directory validation
- configuration validation
- model availability
- administrative boundary validation

---

### Raster Validation

Raster quality assurance includes:

- raster readability
- expected band count
- coordinate reference system verification
- output resolution verification
- radiometric-offset validation
- filename consistency
- cloud-mask verification

---

### Classification Validation

Classification quality assurance includes:

- expected class values
- raster integrity
- model compatibility
- classification completeness

---

### Change Detection Validation

Change detection validation includes:

- report raster generation
- change transition verification
- raster consistency checks
- report availability

---

### Vector Validation

Vector validation includes:

- shapefile completeness
- attribute verification
- feature-count verification
- administrative spatial join
- polygon-area validation
- coordinate validation

The validated pilot implementation produced:

- 729,869 polygons
- 32 attributes
- 100% administrative-area assignment

---

### Repository Validation

Repository quality assurance includes:

- notebook validation
- configuration validation
- Git tracking review
- generated-output separation
- documentation review
- repository cleanup

---

### Validation Philosophy

The workflow follows a staged validation approach.

Every major processing stage must satisfy its quality checks before the next stage begins.

This prevents processing errors from propagating through the remainder of the workflow.

## Known Limitations

The current implementation has been validated as a pilot workflow.

The following limitations are known.

### Processing Scope

The workflow has been fully validated for the BR-163 pilot implementation.

Additional Sentinel-2 tiles have not yet undergone the same level of validation.

---

### External Dependencies

The repository depends on an external PyEO source checkout.

The PyEO source code is intentionally maintained separately.

---

### Credentials

Copernicus Data Space credentials are not distributed with the repository.

Each user must configure local authentication before downloading imagery.

---

### Generated Outputs

Large generated datasets are intentionally excluded from Git.

Operational outputs are regenerated by executing the workflow.

---

### Administrative References

The validated implementation currently performs administrative enrichment using Brazil ADM1 boundaries.

ADM2 and ADM3 integration remain future enhancements.

---

### Coordinate Fields

The current vectorisation implementation stores representative-point coordinates in projected CRS (EPSG:32721).

The attribute names `long` and `lat` therefore represent projected coordinates rather than geographic longitude and latitude.

A future implementation should either:

- rename these fields to `easting` and `northing`, or
- transform representative points to EPSG:4326 before writing them.

---

### Windows Validation

The repository has been validated using Windows.

Additional validation under Linux should be completed before claiming cross-platform operational support.

---

### Future Expansion

Future work will include:

- additional Sentinel-2 tiles
- corridor-wide processing
- reusable QA modules
- automated configuration validation
- release packaging

## Future Roadmap

The current repository represents a validated pilot implementation for the Amazon BR-163 workflow.

Future development is planned in incremental releases.

### Planned Enhancements

#### Workflow

- Extend validation to additional Sentinel-2 tiles.
- Support corridor-wide processing.
- Improve configuration validation.
- Expand automated quality assurance.

#### Source Code

- Improve Windows compatibility.
- Refactor reusable notebook logic into Python modules.
- Improve coordinate-field handling.
- Expand automated testing.

#### Documentation

- Complete engineering documentation.
- Add troubleshooting guides.
- Add workflow diagrams.
- Document common operational scenarios.

#### Repository

- GitHub Releases
- Versioned milestones
- Issue tracking
- Continuous improvement

---

## Release Status

Current release:

**Version 1.0**

Status:

**Validated local implementation**

Completed:

- Windows adaptation
- CDSE integration
- Operational notebooks
- Model training
- Change detection
- Vectorisation
- Administrative enrichment
- Structured QA
- Repository cleanup
- Version control

The repository is now transitioning from implementation to long-term maintenance and incremental improvement.

## License

This project is released under the MIT License.

See the repository root:

```
LICENSE
```

for the complete license text.

The MIT License applies only to original work contained in this repository.

Third-party software, data, and external resources remain subject to their own licenses and terms of use, including:

- PyEO
- Copernicus Sentinel-2 data
- GeoBoundaries
- GDAL
- Rasterio
- GeoPandas

Users are responsible for reviewing and complying with the applicable third-party licenses and data-use conditions.